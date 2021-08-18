echol() {
#
# Print to stdout, optionally to a log file.
# Requires $CREATE_LOGFILE and $LOG_FILE_PATH to be defined.
#
# param $@: args to be printed
#
    echo -e "$@"
    if [[ $CREATE_LOGFILE == "yes" ]]; then
        local timestamp=$(date +"%b %e %H:%M:%S")
        echo -e "${timestamp}: $@" >> "$LOG_FILE_PATH"
    fi
}


exit_with_error() {
    echol $@
    exit 1
}


__check_curl() {
#
# Use curl in silent mode to check if target `url` is available.
#
# param $1: url to be tested
#
    (( $# > 0 )) || exit_with_error "__check_curl: no url provided"
    local url=$1

    echol "Testing connection to: \"${url}\" using curl..."

    err_msg=$(curl --show-error --silent $url 2>&1 >/dev/null) || exit_with_error "curl failed, reason: ($err_msg)"
}


__check_wget() {
#
# Use wget in spider mode (without downloading resources) to check if target `url`
# is available.
#
# param $1: url to be tested
#
    (( $# > 0 )) || exit_with_error "__check_wget: no url provided"
    local url=$1

    echol "Testing connection to: \"${url}\" using wget..."

    err_msg=$(wget --spider --no-directiories $url 2>&1 >/dev/null) || exit_with_error "wget failed, reason: ($err_msg)"
}


__check_apt() {
#
# Use `apt update` to make sure that there is connection to repositories.
#
    echol "Testing apt connection..."

    (( $UID == 0 )) || exit_with_error "apt needs to be run as a root"

    err_msg=$(apt update 2>&1 >/dev/null) || exit_with_error "\"apt update\" failed, reason: ($err_msg)"
}


__check_yum() {
#
# Use `yum list` to make sure that there is connection to repositories.
# Pick first available repo, clean the cache and then query available packages.
#
    echol "Testing yum connection..."

    local repo=$(yum repolist --quiet | tail -n1 | cut -d' ' -f1 | cut -d'/' -f1)

    err_msg=$(yum clean all) || exit_with_error "yum failed, reason: ($err_msg)"

    err_msg=$(yum --quiet --disablerepo=* --enablerepo=$repo list available 2>&1 >/dev/null) \
            || exit_with_error "yum failed, reason: ($err_msg)"
}


__check_crane() {
#
# Use `crane ls` to check if there is a connection to the repository.
#
# param $1: url to be tested
#
    (( $# > 0 )) || exit_with_error "__check_crane: no repository provided"
    local repo=$1

    echol "Testing connection to $repo using crane"
    err_msg=$(crane ls $repo 2>&1 >/dev/null) || exit_with_error "crane failed, reason: ($err_msg)"
}


# Tools which can be tested:
declare -A tools=(
[curl]=__check_curl
[wget]=__check_wget
[apt]=__check_apt
[yum]=__check_yum
[crane]=__check_crane
)


check_connection() {
#
# Run connection test for target `tool` with optional `url` parameter.
# Requires $internet_access_checks_enabled to be defined.
#
# param $1: which `tool` to test
# param $@: optional parameters used by some tools such as `url`
#
    [[ $internet_access_checks_enabled == "no" ]] && return 0

    [[ $# -lt 1 ]] && exit_with_error "(tool) argument not provided"
    local tool=$1

    shift  # discard tool variable

    [[ ! -n ${tools[$tool]} ]] && exit_with_error "no such tool ($tool)"

    ${tools[$tool]} $@

    echol "Connection successful."
}
