#!/usr/bin/env bash

# VERSION 1.0.4

# NOTE: You can run only one instance of this script, new instance kills the previous one
#       This limitation is for Ansible

set -euo pipefail

# === Functions (in alphabetical order) ===

# params: <repo_id> <repo_url>
add_repo() {
	local repo_id="$1"
	local repo_url="$2"

	if ! is_repo_enabled "$repo_id"; then
		echol "Adding repository: $repo_id"
		yum-config-manager --add-repo "$repo_url" ||
			exit_with_error "Command failed: yum-config-manager --add-repo \"$repo_url\""
		# to accept import of GPG keys
		yum -y repolist > /dev/null ||
			exit_with_error "Command failed: yum -y repolist"
	fi
}

# params: <repo_id> <config_file_content>
add_repo_as_file() {
	local repo_id="$1"
	local config_file_content="$2"
	local config_file_name="$repo_id.repo"

	if ! is_repo_enabled "$repo_id"; then
		echol "Adding repository: $repo_id"
		cat <<< "$config_file_content" > "/etc/yum.repos.d/$config_file_name" ||
			exit_with_error "Function add_repo_as_file failed for repo: $repo_id"
		# to accept import of GPG keys
		yum -y repolist > /dev/null || exit_with_error "Command failed: yum -y repolist"
	fi
}

# params: <script_url>
add_repo_from_script() {
	local script_url="$1"

	echol "Running: curl $script_url | bash"
	curl $script_url | bash
}

# params: <backup_file_path> <path_1_to_backup1> ... [path_N_to_backup]
backup_files() {
	local backup_file_path="$1"
	shift
	local paths_to_backup="$@"

	# --directory='/' is for tar --verify
	tar --create --verbose --verify --directory="/" --file="$backup_file_path" $paths_to_backup
}

# params: <dir_path>
create_directory() {
	local dir_path="$1"

	if [[ -d  "$dir_path" ]]; then
		echol "Directory $dir_path already exists"
	else
		echol "Creating directory: $dir_path"
		mkdir -p "$dir_path" || exit_with_error "Command failed: mkdir -p \"$dir_path\""
	fi
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

# params: <file_url> <dest_dir>
download_file() {
	local file_url="$1"
	local dest_dir="$2"

	local file_name=$(basename "$file_url")
	local dest_path="$dest_dir/$file_name"

	# wget with --timestamping sometimes failes on AWS with ERROR 403: Forbidden
	# so we remove existing file to overwrite it, to be optimized
	[[ ! -f $dest_path ]] || remove_file "$dest_path"

	echol "Downloading file: $file"

	wget --no-verbose --directory-prefix="$dest_dir" "$file_url" ||
		exit_with_error "Command failed: wget --no-verbose --directory-prefix=\"$dest_dir\" \"$file_url\""
}

# params: <image_name> <dest_dir>
download_image() {
	local image_name="$1"
	local dest_dir="$2"

	local splited_image=(${image_name//:/ })
	local repository=${splited_image[0]}
	local tag=${splited_image[1]}
	local repo_basename=$(basename -- "$repository")
	local dest_path="${dest_dir}/${repo_basename}-${tag}.tar"

	if [[ -f $dest_path ]]; then
		echol "Image file: "$dest_path" already exists. Skipping..."
	else
		# use temporary file for downloading to be safe from sudden interruptions (network, ctrl+c)
		local tmp_file_path=$(mktemp)
		local skopeo_cmd="$SKOPEO_BIN --insecure-policy copy docker://$image_name docker-archive:$tmp_file_path:$repository:$tag"
		echol "Downloading image: $image"
		# try twice to avoid random error on Azure: "pinging docker registry returned: Get https://k8s.gcr.io/v2/: net/http: TLS handshake timeout"
		{ $skopeo_cmd && chmod 644 $tmp_file_path && mv $tmp_file_path $dest_path; } ||
		{ echol "Second try:" && $skopeo_cmd && chmod 644 $tmp_file_path && mv $tmp_file_path $dest_path; } ||
			exit_with_error "skopeo failed, command was: $skopeo_cmd && chmod 644 $tmp_file_path && mv $tmp_file_path $dest_path"
	fi
}

# params: <dest_dir> <package_1> ... [package_N]
download_packages() {
	local dest_dir="$1"
	shift
	local packages="$@"

	if [[ -n $packages ]]; then
		# when using --archlist=x86_64 yumdownloader (yum-utils-1.1.31-52) also downloads i686 packages
		yumdownloader --quiet --archlist=x86_64 --exclude='*i686' --destdir="$dest_dir" $packages ||
			exit_with_error "yumdownloader failed for: $packages"
	fi
}

echol() {
	echo -e "$@"
	if [[ $CREATE_LOGFILE == 'yes' ]]; then
		local timestamp=$(date +"%b %e %H:%M:%S")
		echo -e "${timestamp}: $@" >> "$LOG_FILE_PATH"
	fi
}

# params: <repo_id>
enable_repo() {
	local repo_id="$1"

	if ! yum repolist enabled | grep --quiet "$repo_id"; then
		echol "Enabling repository: $repo_id"
		yum-config-manager --enable "$repo_id" ||
			exit_with_error "Command failed: yum-config-manager --enable \"$repo_id\""
	fi
}

exit_with_error() {
	echol "ERROR: $1"
	exit 1
}

# desc: find repo id (set $1) based on given pattern
# params: <result_var> <rhel_on_prem_repo_id> <extended_regexp>
find_rhel_repo_id() {
	# $1 reserved for result
	local rhel_on_prem_repo_id="$2"
	local pattern="$3"
	local repo_id

	if yum repolist all | egrep --quiet "$pattern"; then
		repo_id=$(yum repolist all | egrep --only-matching "$pattern")
	else
		exit_with_error "RHEL yum repository not found, pattern was: $pattern"
	fi

	eval $1='$repo_id'
}

# params: <result_var> <package>
get_package_dependencies_with_arch() {
	# $1 reserved for result
	local package="$2"

	local query_output=$(repoquery --requires --resolve --queryformat '%{name}.%{arch}' --archlist=x86_64,noarch "$package") ||
		exit_with_error "repoquery failed for dependencies of package: $package with exit code: $?, output was: $query_output"

	if [[ -z $query_output ]]; then
		echol "No dependencies found for package: $package"
	elif grep --ignore-case --perl-regexp '\b(?<!-)error(?!-)\b' <<< "$query_output"; then
		exit_with_error "repoquery failed for dependencies of package: $package, output was: $query_output"
	fi

	eval $1='($query_output)'
}

# desc: get full package name with version and architecture
# params: <result_var> <package>
get_package_with_version_arch() {
	# $1 reserved for result
	local package="$2"

	local query_output=$(repoquery --queryformat '%{ui_nevra}' --archlist=x86_64,noarch "$package") ||
		exit_with_error "repoquery failed for package: $package with exit code: $?, output was: $query_output"

	# yumdownloader doesn't set error code if repoquery returns empty output
	[[ -n $query_output ]] || exit_with_error "repoquery failed: package $package not found"
	if grep --ignore-case --perl-regexp '\b(?<!-)error(?!-)\b' <<< "$query_output"; then
		exit_with_error "repoquery failed for package: $package, output was: $query_output"
	else
		echol "Found: $query_output"
	fi

	eval $1='$query_output'
}

# params: <result_var> <packages_array>
get_packages_with_version_arch() {
	local result_var_name="$1"
	shift
	local packages=("$@")
	local packages_with_version_arch=()

	for package in "${packages[@]}"; do
		get_package_with_version_arch 'QUERY_OUTPUT' "$package"
		packages_with_version_arch+=("$QUERY_OUTPUT")
	done

	eval $result_var_name='("${packages_with_version_arch[@]}")'
}

# params: <result_var> <group_name> <requirements_file_path>
get_requirements_from_group() {
	# $1 reserved for result
	local group_name="$2"
	local requirements_file_path="$3"

	local all_requirements=$(grep --only-matching '^[^#]*' "$requirements_file_path" | sed -e 's/[[:space:]]*$//')
	local requirements_from_group=$(awk "/^$/ {next}; /\[${group_name}\]/ {f=1; next}; /^\[/ {f=0}; f {print \$0}" <<< "$all_requirements") ||
		exit_with_error "Function get_requirements_from_group failed for group: $group_name"

	[[ -n $requirements_from_group ]] || echol "No requirements found for group: $group_name"

	eval $1='$requirements_from_group'
}

# params: <result_var> <array>
get_unique_array() {
	local result_var_name="$1"
	shift
	local array=("$@")

	# filter out duplicates
	array=($(echo "${array[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' '))

	eval $result_var_name='("${array[@]}")'
}

# params: <package_name_or_url> [package_name]
install_package() {
	local package_name_or_url="$1"
	local package_name="$1"

	[ $# -gt 1 ] && package_name="$2"

	echol "Installing package: $package_name"
	if yum install -y "$package_name_or_url"; then
		echo "$package_name" >> "$INSTALLED_PACKAGES_FILE_PATH"
	else
		exit_with_error "Command failed: yum install -y \"$package_name_or_url\""
	fi
}

# params: <package>
is_package_installed() {
	local package="$1"

	if rpm --query --quiet "$package"; then
		echol "Package $package already installed"
		return 0
	else
		return 1
	fi
}

# params: <repo_id>
is_repo_available() {
	local repo_id="$1"

	echol "Checking if '$repo_id' repo is available"
	yum -q --disablerepo=* --enablerepo="$repo_id" repoinfo > /dev/null # returns 1 when 'Error 404 - Not Found'
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

# params: <package>
remove_package() {
	local package="$1"

	if rpm --query --quiet "$package"; then
		echol "Removing package: $package"
		yum remove -y "$package" || exit_with_error "Command failed: yum remove -y \"$package\""
	fi
}

# params: <yum_repos_backup_tar_file_path>
remove_added_repos() {
	local yum_repos_backup_tar_file_path="$1"

	declare -A initial_yum_repo_files
	for repo_config_file in $(tar -tf "$yum_repos_backup_tar_file_path" | grep '.repo$' | xargs -L 1 --no-run-if-empty basename); do
		initial_yum_repo_files["$repo_config_file"]=1
	done

	for repo_config_file in $(find /etc/yum.repos.d/ -maxdepth 1 -type f -name '*.repo' -printf "%f\n"); do
		if (( ${initial_yum_repo_files["$repo_config_file"]:-0} == 0)); then
			# remove only if not owned by a package
			if ! rpm --quiet --query --file "/etc/yum.repos.d/$repo_config_file"; then
				remove_file "/etc/yum.repos.d/$repo_config_file"
			fi
		fi
	done
}

# params: <file_path>
remove_file() {
	local file_path="$1"

	echol "Removing file: $file_path"
	rm -f "$file_path" || exit_with_error "Command failed: rm -f \"$file_path\""
}

# params: <installed_packages_list_file_path>
remove_installed_packages() {
	local installed_packages_list_file="$1"

	if [ -f "$installed_packages_list_file" ]; then
		for package in $(cat $installed_packages_list_file | sort --unique); do
			remove_package "$package"
		done
		remove_file "$installed_packages_list_file"
	fi
}

# params: <command to execute>
run_cmd() {
	local cmd_arr=("$@")

	echol "Executing: ${cmd_arr[*]}"
	"${cmd_arr[@]}" || exit_with_error "Command failed: ${cmd_arr[*]}"
}

usage() {
	echo "usage: ./$(basename $0) <downloads_dir>"
	echo "       ./$(basename $0) /tmp/downloads"
	[ -z "$1" ] || exit "$1"
}

# === Start ===

[ $# -gt 0 ] || usage 1 >&2
readonly START_TIME=$(date +%s)

# --- Parse arguments ---

POSITIONAL_ARGS=()
CREATE_LOGFILE='yes'
while [[ $# -gt 0 ]]; do
case $1 in
	--no-logfile)
	CREATE_LOGFILE='no'
	shift # past argument
	;;
	*) # unknown option
	POSITIONAL_ARGS+=("$1") # save it in an array for later
	shift
	;;
esac
done
set -- "${POSITIONAL_ARGS[@]}" # restore positional arguments

# --- Global variables ---

# dirs
readonly DOWNLOADS_DIR="$1" # root directory for downloads
readonly FILES_DIR="$DOWNLOADS_DIR/files"
readonly PACKAGES_DIR="$DOWNLOADS_DIR/packages"
readonly IMAGES_DIR="$DOWNLOADS_DIR/images"
readonly REPO_PREREQ_PACKAGES_DIR="$PACKAGES_DIR/repo-prereqs"
readonly SCRIPT_DIR="$(dirname $(readlink -f $0))" # want absolute path

# files
readonly REQUIREMENTS_FILE_PATH="$SCRIPT_DIR/requirements.txt"
readonly SCRIPT_FILE_NAME=$(basename $0)
readonly LOG_FILE_NAME=${SCRIPT_FILE_NAME/sh/log}
readonly LOG_FILE_PATH="$SCRIPT_DIR/$LOG_FILE_NAME"
readonly YUM_CONFIG_BACKUP_FILE_PATH="$SCRIPT_DIR/${SCRIPT_FILE_NAME}-yum-repos-backup-tmp-do-not-remove.tar"
readonly SKOPEO_BIN="$SCRIPT_DIR/skopeo_linux"
readonly INSTALLED_PACKAGES_FILE_PATH="$SCRIPT_DIR/${SCRIPT_FILE_NAME}-installed-packages-list-do-not-remove.tmp"
readonly PID_FILE_PATH=/var/run/${SCRIPT_FILE_NAME/sh/pid}

# --- Checks ---

[ $EUID -eq 0 ] || { echo "You have to run as root" && exit 1; }

[[ -f $REQUIREMENTS_FILE_PATH ]] || exit_with_error "File not found: $REQUIREMENTS_FILE_PATH"
[[ -f $SKOPEO_BIN ]] || exit_with_error "File not found: $SKOPEO_BIN"
[[ -x $SKOPEO_BIN ]] || exit_with_error "$SKOPEO_BIN have to be executable"

# --- Want to have only one instance for Ansible ---

if [ -f $PID_FILE_PATH ]; then
	readonly PID_FROM_FILE=$(cat $PID_FILE_PATH 2> /dev/null)
	if [[ -n $PID_FROM_FILE ]] && kill -0 $PID_FROM_FILE > /dev/null 2>&1; then
		echol "Found running process with pid: $PID_FROM_FILE, cmd: $(ps -p $PID_FROM_FILE -o cmd=)"
		if ps -p $PID_FROM_FILE -o cmd= | grep --quiet $SCRIPT_FILE_NAME; then
			echol "Killing old instance using SIGTERM"
			kill -s SIGTERM $PID_FROM_FILE # try gracefully
			if sleep 3 && kill -0 $PID_FROM_FILE > /dev/null 2>&1; then
				echol "Still running, killing old instance using SIGKILL"
				kill -s SIGKILL $PID_FROM_FILE # forcefully
			fi
		else
			remove_file $PID_FILE_PATH
			exit_with_error "Process with pid: $PID_FILE_PATH seems to be not an instance of this script"
		fi
	else
		echol "Process with pid: $PID_FROM_FILE not found"
	fi
	remove_file $PID_FILE_PATH
fi

echol "PID is: $$, creating file: $PID_FILE_PATH"
echo $$ > $PID_FILE_PATH || exit_with_error "Command failed: echo $$ > $PID_FILE_PATH"

# --- Parse requirements file ---

# Requirements are grouped using sections: [packages-repo-prereqs], [packages], [files], [images]
get_requirements_from_group 'REPO_PREREQ_PACKAGES' 'packages-repo-prereqs' "$REQUIREMENTS_FILE_PATH"
get_requirements_from_group 'PACKAGES'             'packages'              "$REQUIREMENTS_FILE_PATH"
get_requirements_from_group 'FILES'                'files'                 "$REQUIREMENTS_FILE_PATH"
get_requirements_from_group 'IMAGES'               'images'                "$REQUIREMENTS_FILE_PATH"

# === Packages ===

# --- Backup yum repositories ---

if [ -f "$YUM_CONFIG_BACKUP_FILE_PATH" ]; then
	echol "Backup aleady exists: $YUM_CONFIG_BACKUP_FILE_PATH"
else
	echol "Backuping /etc/yum.repos.d/ to $YUM_CONFIG_BACKUP_FILE_PATH"
	if backup_files "$YUM_CONFIG_BACKUP_FILE_PATH" '/etc/yum.repos.d/'; then
		echol "Backup done"
	else
		if [ -f "$YUM_CONFIG_BACKUP_FILE_PATH" ]; then
			remove_file "$YUM_CONFIG_BACKUP_FILE_PATH"
		fi
		exit_with_error "Backup of yum repositories failed"
	fi
fi

# --- Install required packages unless present ---

# repos can be enabled or disabled using the yum-config-manager command, which is provided by yum-utils package
for package in 'yum-utils' 'wget' 'curl'; do
	if ! is_package_installed "$package"; then
		install_package "$package"
	fi
done

# --- Enable RHEL repos ---

# -> rhel-7-server-extras-rpms # for container-selinux package, this repo has different id names on clouds
# About rhel-7-server-extras-rpms: https://access.redhat.com/solutions/3418891

ON_PREM_REPO_ID='rhel-7-server-extras-rpms'
REPO_ID_PATTERN="$ON_PREM_REPO_ID|rhui-REGION-rhel-server-extras|rhui-rhel-7-server-rhui-extras-rpms" # on-prem|AWS|Azure
find_rhel_repo_id 'REPO_ID' "$ON_PREM_REPO_ID" "$REPO_ID_PATTERN"
enable_repo "$REPO_ID"

# -> rhel-server-rhscl-7-rpms # for Red Hat Software Collections (RHSCL), this repo has different id names on clouds
# About rhel-server-rhscl-7-rpms: https://access.redhat.com/solutions/472793

ON_PREM_REPO_ID='rhel-server-rhscl-7-rpms'
REPO_ID_PATTERN="$ON_PREM_REPO_ID|rhui-REGION-rhel-server-rhscl|rhui-rhel-server-rhui-rhscl-7-rpms" # on-prem|AWS|Azure
find_rhel_repo_id 'REPO_ID' "$ON_PREM_REPO_ID" "$REPO_ID_PATTERN"
enable_repo "$REPO_ID"

# --- Add repos ---

DOCKER_CE_FALLBACK_REPO_CONF=$(cat <<'EOF'
[docker-ce-stable-fallback]
name=Docker CE Stable - fallback centos/7/x86_64/stable
baseurl=https://download.docker.com/linux/centos/7/x86_64/stable
enabled=1
gpgcheck=1
gpgkey=https://download.docker.com/linux/centos/gpg
EOF
)

ELASTIC_6_REPO_CONF=$(cat <<'EOF'
[elastic-6]
name=Elastic repository for 6.x packages
baseurl=https://artifacts.elastic.co/packages/oss-6.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF
)

ELASTICSEARCH_7_REPO_CONF=$(cat <<'EOF'
[elasticsearch-7.x]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/oss-7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF
)

ELASTICSEARCH_CURATOR_REPO_CONF=$(cat <<'EOF'
[curator-5]
name=CentOS/RHEL 7 repository for Elasticsearch Curator 5.x packages
baseurl=https://packages.elastic.co/curator/5/centos/7
gpgcheck=1
gpgkey=https://packages.elastic.co/GPG-KEY-elasticsearch
enabled=1
EOF
)

GRAFANA_REPO_CONF=$(cat <<'EOF'
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF
)

KUBERNETES_REPO_CONF=$(cat <<'EOF'
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
)

OPENDISTRO_REPO_CONF=$(cat <<'EOF'
[opendistroforelasticsearch-artifacts-repo]
name=Release RPM artifacts of OpenDistroForElasticsearch
baseurl=https://d3g5vo6xdbdb9a.cloudfront.net/yum/noarch/
enabled=1
gpgkey=https://d3g5vo6xdbdb9a.cloudfront.net/GPG-KEY-opendistroforelasticsearch
gpgcheck=1
repo_gpgcheck=1
autorefresh=1
type=rpm-md
EOF
)

POSTGRESQL_REPO_CONF=$(cat <<'EOF'
[pgdg10]
name=PostgreSQL 10 for RHEL/CentOS $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG
EOF
)

RABBITMQ_ERLANG_REPO_CONF=$(cat <<'EOF'
[rabbitmq_erlang]
name=rabbitmq_erlang
baseurl=https://packagecloud.io/rabbitmq/erlang/el/7/$basearch
repo_gpgcheck=1
gpgcheck=1
enabled=1
gpgkey=https://packagecloud.io/rabbitmq/erlang/gpgkey
EOF
)

RABBITMQ_SERVER_REPO_CONF=$(cat <<'EOF'
[rabbitmq_rabbitmq-server]
name=rabbitmq_rabbitmq-server
baseurl=https://packagecloud.io/rabbitmq/rabbitmq-server/el/7/$basearch
repo_gpgcheck=1
gpgcheck=1
enabled=1
gpgkey=https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey
EOF
)

add_repo 'docker-ce' 'https://download.docker.com/linux/centos/docker-ce.repo'
# occasionally docker-ce repo (at https://download.docker.com/linux/centos/7Server/x86_64/stable) is unavailable
if ! is_repo_available "docker-ce-stable"; then
	disable_repo "docker-ce-stable"
	add_repo_as_file 'docker-ce-stable-fallback' "$DOCKER_CE_FALLBACK_REPO_CONF"
fi
add_repo_as_file 'elastic-6' "$ELASTIC_6_REPO_CONF"
add_repo_as_file 'elasticsearch-7' "$ELASTICSEARCH_7_REPO_CONF"
add_repo_as_file 'elasticsearch-curator-5' "$ELASTICSEARCH_CURATOR_REPO_CONF"
add_repo_as_file 'grafana' "$GRAFANA_REPO_CONF"
add_repo_as_file 'kubernetes' "$KUBERNETES_REPO_CONF"
add_repo_as_file 'opendistroforelasticsearch' "$OPENDISTRO_REPO_CONF"
add_repo_as_file 'postgresql-10' "$POSTGRESQL_REPO_CONF"
add_repo_as_file 'rabbitmq_erlang' "$RABBITMQ_ERLANG_REPO_CONF"
add_repo_as_file 'rabbitmq_rabbitmq-server' "$RABBITMQ_SERVER_REPO_CONF"
add_repo_from_script 'https://dl.2ndquadrant.com/default/release/get/10/rpm'
disable_repo '2ndquadrant-dl-default-release-pg10-debug'

# some packages are from EPEL repo
if ! is_package_installed 'epel-release'; then
	install_package 'https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm' 'epel-release'
fi

run_cmd yum -y makecache fast

# --- Download packages ---

# 1) packages required to create repository

create_directory "$REPO_PREREQ_PACKAGES_DIR"

# prepare lists
PREREQ_PACKAGES=()
for package in $REPO_PREREQ_PACKAGES; do
	echol "Processing package: $package"
	get_package_with_version_arch 'QUERY_OUTPUT' "$package"
	PREREQ_PACKAGES+=("$QUERY_OUTPUT")
done

# download requirements (fixed versions)
if [[ ${#PREREQ_PACKAGES[@]} -gt 0 ]]; then
	echol "Downloading repository prerequisite packages (${#PREREQ_PACKAGES[@]})..."
	download_packages "$REPO_PREREQ_PACKAGES_DIR" "${PREREQ_PACKAGES[@]}"
fi

# 2) non-prerequisite packages

create_directory "$PACKAGES_DIR"

# prepare lists
NON_PREREQ_PACKAGES=()
DEPENDENCIES_OF_NON_PREREQ_PACKAGES=()
for package in $PACKAGES; do
	echol "Processing package: $package"
	get_package_with_version_arch 'QUERY_OUTPUT' "$package"
	NON_PREREQ_PACKAGES+=("$QUERY_OUTPUT")
	get_package_dependencies_with_arch 'DEPENDENCIES' "$package"
	if [[ ${#DEPENDENCIES[@]} -gt 0 ]]; then
		for dependency in "${DEPENDENCIES[@]}"; do
			DEPENDENCIES_OF_NON_PREREQ_PACKAGES+=("$dependency")
		done
	fi
done

if [[ ${#NON_PREREQ_PACKAGES[@]} -gt 0 ]]; then
	# download requirements (fixed versions)
	echol "Downloading packages (${#NON_PREREQ_PACKAGES[@]})..."
	download_packages "$PACKAGES_DIR" "${NON_PREREQ_PACKAGES[@]}"
	# download dependencies (latest versions)
	get_unique_array 'DEPENDENCIES' "${DEPENDENCIES_OF_NON_PREREQ_PACKAGES[@]}"
	get_packages_with_version_arch 'DEPENDENCIES' "${DEPENDENCIES[@]}"
	echol "Downloading dependencies of packages (${#DEPENDENCIES[@]})..."
	download_packages "$PACKAGES_DIR" "${DEPENDENCIES[@]}"
fi

# --- Clean up yum repos ---

remove_added_repos "$YUM_CONFIG_BACKUP_FILE_PATH"

# --- Restore yum repos ---

echol "Restoring /etc/yum.repos.d/*.repo from: $YUM_CONFIG_BACKUP_FILE_PATH"
echol "Executing: tar --extract --verbose --file $YUM_CONFIG_BACKUP_FILE_PATH"
if tar --extract --verbose --file "$YUM_CONFIG_BACKUP_FILE_PATH" --directory /etc/yum.repos.d \
		--strip-components=2 etc/yum.repos.d/*.repo; then
	echol "Restored: yum repositories"
else
	exit_with_error "Extracting tar failed: $YUM_CONFIG_BACKUP_FILE_PATH"
fi

# === Files ===

create_directory "$FILES_DIR"

for file in $FILES; do
	download_file "$file" "$FILES_DIR"
done

# === Images ===

create_directory "$IMAGES_DIR"

for image in $IMAGES; do
	download_image "$image" "$IMAGES_DIR"
done

# --- Clean up ---

remove_installed_packages "$INSTALLED_PACKAGES_FILE_PATH"

remove_file "$YUM_CONFIG_BACKUP_FILE_PATH"

remove_file "$PID_FILE_PATH"

readonly END_TIME=$(date +%s)

echol "$(basename $0) finished, execution time: $(date -u -d @$((END_TIME-START_TIME)) +'%Hh:%Mm:%Ss')"