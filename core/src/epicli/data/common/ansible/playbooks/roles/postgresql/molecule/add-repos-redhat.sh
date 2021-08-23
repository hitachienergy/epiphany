#!/usr/bin/env bash

set -euo pipefail

CREATE_LOGFILE='no'

# params: <repo_id> <config_file_content>
add_repo_as_file() {
    local repo_id="$1"
    local config_file_content="$2"
    local config_file_name="$repo_id.repo"

    if ! is_repo_enabled "$repo_id"; then
        echol "Adding repository: $repo_id"
        cat <<<"$config_file_content" >"/etc/yum.repos.d/$config_file_name" ||
            exit_with_error "Function add_repo_as_file failed for repo: $repo_id"
        local -a gpg_key_urls
        IFS=" " read -r -a gpg_key_urls \
            <<<"$(grep -i --only-matching --perl-regexp '(?<=^gpgkey=)http[^#\n]+' <<<"$config_file_content")"
        if ((${#gpg_key_urls[@]} > 0)); then
            import_repo_gpg_keys "${gpg_key_urls[@]}" 3
        fi
        # to accept import of repo's GPG key (for repo_gpgcheck=1)
        yum -y repolist >/dev/null || exit_with_error "Command failed: yum -y repolist"
    fi
}

# params: <script_url>
add_repo_from_script() {
    local script_url="$1"

    echol "Running: curl $script_url | bash"
    curl $script_url | bash
}

# params: <repo_id>
disable_repo() {
    local repo_id="$1"

    if yum repolist enabled | grep --quiet "$repo_id"; then
        echol "Disabling repository: $repo_id"
        yum-config-manager --disable "$repo_id" ||
            exit_with_error "Command failed: yum-config-manager --disable \"$repo_id\""
    fi
}

echol() {
    echo -e "$@"
    if [[ $CREATE_LOGFILE == 'yes' ]]; then
        local timestamp=$(date +"%b %e %H:%M:%S")
        echo -e "${timestamp}: $@" >>"$LOG_FILE_PATH"
    fi
}

# params: <url(s)> <retries>
import_repo_gpg_keys() {
    local retries=${!#}        # get last arg
    local urls=("${@:1:$#-1}") # remove last arg

    for url in "${urls[@]}"; do
        run_cmd_with_retries rpm --import "$url" "$retries"
    done
}

# params: <repo_id>
is_repo_enabled() {
    local repo_id="$1"

    if yum repolist | grep --quiet "$repo_id"; then
        echol "Repository $repo_id already enabled"
        return 0
    else
        return 1
    fi
}

# Runs command as array with printing it, doesn't support commands with shell operators (such as pipe or redirection)
# params: <command to execute> [--no-exit-on-error]
run_cmd() {
    local cmd_arr=("$@")

    local exit_on_error=1
    if [[ ${cmd_arr[-1]} == '--no-exit-on-error' ]]; then
        exit_on_error=0
        cmd_arr=("${cmd_arr[@]:0:$#-1}") # remove last item
    fi

    local escaped_string return_code
    escaped_string=$(_print_array_as_shell_escaped_string "${cmd_arr[@]}")
    echol "Executing: ${escaped_string}"
    "${cmd_arr[@]}"
    return_code=$?
    if ((return_code != 0)) && ((exit_on_error)); then
        exit_with_error "Command failed: ${escaped_string}"
    else
        return $return_code
    fi
}

# Runs command with retries, doesn't support commands with shell operators (such as pipe or redirection)
# params: <command to execute> <retries>
run_cmd_with_retries() {
    # pop 'retries' argument
    local retries=${!#}  # get last arg (indirect expansion)
    set -- "${@:1:$#-1}" # set new "$@"

    local cmd_arr=("$@")
    (# sub-shell is used to limit scope for 'set +e'
        set +e
        trap - ERR # disable global trap locally
        for ((i = 0; i <= retries; i++)); do
            run_cmd "${cmd_arr[@]}" '--no-exit-on-error'
            return_code=$?
            if ((return_code == 0)); then
                break
            elif ((i < retries)); then
                sleep 1
                echol "retrying ($((i + 1))/${retries})"
            else
                echol "ERROR: all attempts failed"
                local escaped_string
                escaped_string=$(_print_array_as_shell_escaped_string "${cmd_arr[@]}")
                exit_with_error "Command failed: ${escaped_string}"
            fi
        done
        return $return_code
    )
}

POSTGRESQL_REPO_CONF=$(cat <<'EOF'
[pgdg13]
name=PostgreSQL 13 for RHEL/CentOS $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/13/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG
EOF
)

POSTGRESQL_COMMON_REPO_CONF=$(cat <<'EOF'
[pgdg-common]
name=PostgreSQL common for RHEL/CentOS $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/common/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG
EOF
)

add_repo_as_file 'postgresql-13' "$POSTGRESQL_REPO_CONF"
add_repo_as_file 'postgresql-common' "$POSTGRESQL_COMMON_REPO_CONF"          # for pgbouncer
add_repo_from_script 'https://dl.2ndquadrant.com/default/release/get/13/rpm' # for repmgr
disable_repo '2ndquadrant-dl-default-release-pg13-debug'                     # script adds 2 repositories, only 1 is required
