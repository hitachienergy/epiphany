#!/usr/bin/env bash

# Note: Run this script as super user (sudo) and being in the same directory as the script

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
		ADDED_REPOSITORIES+=("$repo_id.repo")
		# to accept import of GPG keys
		yum -y repolist > /dev/null ||
			exit_with_error "Command failed: yum -y repolist"
	fi
}

# params: <repo_id> <config_file_contents>
add_repo_as_file() {
	local repo_id="$1"
	local config_file_contents="$2"
	local config_file_name="$repo_id.repo"

	if ! is_repo_enabled "$repo_id"; then
		echol "Adding repository: $repo_id"
		cat <<< "$config_file_contents" > "/etc/yum.repos.d/$config_file_name" ||
			exit_with_error "Function add_repo_as_file failed for repo: $repo_id"
		ADDED_REPOSITORIES+=("$config_file_name")
		# to accept import of GPG keys
		yum -y repolist > /dev/null || exit_with_error "Command failed: yum -y repolist"
	fi
}

# params: <backup_file_path> <path_1_to_backup1> ... [path_N_to_backup]
backup_files() {
	local backup_file_path="$1"
	shift
	local paths_to_backup="$@"

	backup_file_path=$(readlink -f "$backup_file_path") # make sure it's absolute path
	# cd / is for tar --verify
	(cd / && tar --create --verbose --verify --file="$backup_file_path" $paths_to_backup) || return 1
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

# params: <image_name> <dest_dir>
download_image() {
	local image_name="$1"
	local dest_dir="$2"

	local splited_image=(${image_name//:/ })
	local repository=${splited_image[0]}
	local tag=${splited_image[1]}
	local repo_basename=$(basename -- "$repository")
	local dest_path="${dest_dir}/${repo_basename}-${tag}"

	[[ ! -f $dest_path ]] || remove_file "$dest_path"

	echol "Downloading image: $image"
	./skopeo_linux --insecure-policy copy docker://$image_name docker-archive:$dest_path:$repository:$tag ||
		exit_with_error "skopeo failed, command was: ./skopeo_linux --insecure-policy copy docker://$image_name docker-archive:$dest_path:$repository:$tag"
}

# params: <dest_dir> <package_1> ... [package_N]
download_packages() {
	local dest_dir="$1"
	shift
	local packages="$@"

	if [[ -n $packages ]]; then
		yumdownloader --quiet --destdir "$dest_dir" $packages || exit_with_error "yumdownloader failed for: $packages"
	fi
}

echol() {
	echo -e "$1" | tee --append $LOG_FILE_NAME
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

# params: <result_var> <rhel_on_prem_repo_id> <extended_regexp>
# desc: find repo id (set $1) based on given pattern
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
get_package_dependencies() {
	# $1 reserved for result
	local package="$2"

	local query_output=$(repoquery --requires --resolve --all --queryformat '%{ui_nevra}' --archlist=x86_64,noarch "$package" 2>&1) ||
		exit_with_error "repoquery failed for dependencies of package: $package"

	if [[ -z $query_output ]]; then
		echol "No dependencies found for package: $package"
	elif grep -i 'error' <<< "$query_output"; then
		exit_with_error "repoquery failed for dependencies of package: $package, output was: $query_output"
	fi

	eval $1='$query_output'
}

# params: <result_var> <package>
get_package_with_version() {
	# $1 reserved for result
	local package="$2"

	local query_output=$(repoquery --all --queryformat '%{ui_nevra}' --archlist=x86_64,noarch "$package" 2>&1) ||
		exit_with_error "repoquery failed for package: $package"

	# yumdownloader doesn't handle error codes properly if repoquery gets empty output
	[[ -n $query_output ]] || exit_with_error "repoquery failed: package $package not found"
	if grep -i 'error' <<< "$query_output"; then
		exit_with_error "repoquery failed for package: $package, output was: $query_output"
	else
		echol "Found: $query_output"
	fi

	eval $1='$query_output'
}

# params: <result_var> <group_name> <requirements_file_name>
get_requirements_from_group() {
	# $1 reserved for result
	local group_name="$2"
	local requirements_file_name="$3"

	local all_requirements=$(grep --invert-match '^#' "$requirements_file_name")
	local requirements_from_group=$(awk "/^$/ {next}; /\[${group_name}\]/ {f=1; next}; /^\[/ {f=0}; f {print \$0}" <<< "$all_requirements") ||
		exit_with_error "Function get_requirements_from_group failed for group: $group_name"

	[[ -n $requirements_from_group ]] || echol "No requirements found for group: $group_name"

	eval $1='$requirements_from_group'
}

# params: <package_name_or_url>
install_package() {
	local package="$1"

	echol "Installing package: $package"
	if yum install -y "$package"; then
		INSTALLED_PACKAGES+=("$package")
	else
		exit_with_error "Command failed: yum install -y \"$package\""
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

# params: <array_with_repo_file_names>
remove_added_repos() {
	local added_repos_arr=("$@")

	for repo_config_file in "${added_repos_arr[@]}"; do
		remove_file "/etc/yum.repos.d/$repo_config_file"
	done
}

# params: <file_path>
remove_file() {
	local file_path="$1"

	echol "Removing file: $file_path"
	rm -f "$file_path" || exit_with_error "Command failed: rm -f \"$file_path\""
}

usage() {
	echo "usage: ./$(basename $0) <download_dir>"
	echo "       ./$(basename $0) /tmp/downloads"
	[ -z "$1" ] || exit "$1"
}

# === Start ===

# --- Global variables ---

# dirs
readonly DOWNLOAD_DIR="$1" # root directory for downloads
readonly FILES_DIR=$DOWNLOAD_DIR/files
readonly PACKAGES_DIR=$DOWNLOAD_DIR/packages
readonly IMAGES_DIR=$DOWNLOAD_DIR/images
readonly OFFLINE_PREREQ_PACKAGES_DIR=$PACKAGES_DIR/offline-prereqs

# files
readonly REQUIREMENTS_FILE_NAME=requirements.txt
LOG_FILE_NAME=$(basename $0); readonly LOG_FILE_NAME=${LOG_FILE_NAME/sh/log}
YUM_CONFIG_BACKUP_FILE_PATH=./yum-config-backup.tar
readonly YUM_CONFIG_BACKUP_FILE_PATH=$(readlink -f "$YUM_CONFIG_BACKUP_FILE_PATH") # convert to absolute path

# others
ADDED_REPOSITORIES=()
INSTALLED_PACKAGES=()

# --- Checks ---

[ $# -gt 0 ] || usage 1 >&2

[ $EUID -eq 0 ] || { echo "You have to run as super user" && exit 1; }

# Check if requirements file exists
[[ -f ./$REQUIREMENTS_FILE_NAME ]] || exit_with_error "File not found in the current directory: $REQUIREMENTS_FILE_NAME"

# --- Parse requirements file ---

# Requirements are grouped using sections: [packages-offline-prereqs], [packages], [files], [images]
get_requirements_from_group 'OFFLINE_PREREQ_PACKAGES' 'packages-offline-prereqs' "$REQUIREMENTS_FILE_NAME"
get_requirements_from_group 'PACKAGES'                'packages'                 "$REQUIREMENTS_FILE_NAME"
get_requirements_from_group 'FILES'                   'files'                    "$REQUIREMENTS_FILE_NAME"
get_requirements_from_group 'IMAGES'                  'images'                   "$REQUIREMENTS_FILE_NAME"

# === Packages ===

# --- Backup of repos and yum config ---

if [ -f $YUM_CONFIG_BACKUP_FILE_PATH ]; then
	echol "Backup aleady exists: $YUM_CONFIG_BACKUP_FILE_PATH"
else
	echol "Backuping /etc/yum.repos.d/ and /etc/yum/ to $YUM_CONFIG_BACKUP_FILE_PATH"
	if backup_files $YUM_CONFIG_BACKUP_FILE_PATH '/etc/yum.repos.d/' '/etc/yum/'; then
		echol "Backup done"
	else
		[ ! -f $YUM_CONFIG_BACKUP_FILE_PATH ] ||
			{ echol "Executing: rm -f $YUM_CONFIG_BACKUP_FILE_PATH" && rm -f $YUM_CONFIG_BACKUP_FILE_PATH; }
		exit_with_error "Backup of yum config failed"
	fi
fi

# --- Install required packages unless present ---

# repos can be enabled or disabled using the yum-config-manager command, which is provided by yum-utils package
for package in 'yum-utils' 'wget'; do
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

ELASTIC_REPO_CONF=$(cat <<'EOF'
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
add_repo_as_file 'elastic-6' "$ELASTIC_REPO_CONF"
add_repo_as_file 'curator-5' "$ELASTICSEARCH_CURATOR_REPO_CONF"
add_repo_as_file 'grafana' "$GRAFANA_REPO_CONF"
add_repo_as_file 'kubernetes' "$KUBERNETES_REPO_CONF"
add_repo_as_file 'rabbitmq_erlang' "$RABBITMQ_ERLANG_REPO_CONF"
add_repo_as_file 'rabbitmq_rabbitmq-server' "$RABBITMQ_SERVER_REPO_CONF"

# fping package is a part of EPEL repo
if ! is_package_installed 'epel-release'; then
	install_package 'https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm'
fi

echol "Executing: yum -y makecache fast" && yum -y makecache fast

# --- Download packages ---

create_directory "$OFFLINE_PREREQ_PACKAGES_DIR"
create_directory "$PACKAGES_DIR"

for package in $OFFLINE_PREREQ_PACKAGES; do
	echol "Processing package: $package"
	get_package_with_version 'QUERY_OUTPUT' "$package"
	download_packages "$OFFLINE_PREREQ_PACKAGES_DIR" $QUERY_OUTPUT
	# download package dependencies if exist
	get_package_dependencies 'QUERY_OUTPUT' "$package"
	download_packages "$OFFLINE_PREREQ_PACKAGES_DIR" $QUERY_OUTPUT
done

for package in $PACKAGES; do
	echol "Processing package: $package"
	get_package_with_version 'QUERY_OUTPUT' "$package"
	download_packages "$PACKAGES_DIR" $QUERY_OUTPUT
	# download package dependencies if exist
	get_package_dependencies 'QUERY_OUTPUT' "$package"
	download_packages "$PACKAGES_DIR" $QUERY_OUTPUT
done

# --- Clean up yum repos ---

if [ ${#ADDED_REPOSITORIES[@]} -gt 0 ]; then
	remove_added_repos "${ADDED_REPOSITORIES[@]}"
fi

# --- Restore yum repos ---

if [ -f $YUM_CONFIG_BACKUP_FILE_PATH ]; then
	echol "Restoring /etc/yum.repos.d/*.repo from: $YUM_CONFIG_BACKUP_FILE_PATH"
	echol "Executing: tar --extract --verbose --file $YUM_CONFIG_BACKUP_FILE_PATH ..."
	if tar --extract --verbose --file $YUM_CONFIG_BACKUP_FILE_PATH --directory /etc/yum.repos.d \
			--strip-components=2 etc/yum.repos.d/*.repo; then
		echol "Restored: yum repositories"
		remove_file $YUM_CONFIG_BACKUP_FILE_PATH
	else
		exit_with_error "Extracting tar failed"
	fi
fi


# === Files ===

create_directory "$FILES_DIR"

for file in $FILES; do
	echol "Downloading file: $file"
	# on AWS --timestamping gives 'ERROR 403: Forbidden', so --recursive is used to force overwriting
	wget --recursive --no-verbose  --directory-prefix="$FILES_DIR" "$file" ||
		exit_with_error "Command failed: wget --recursive --no-verbose --directory-prefix=\"$FILES_DIR\" \"$file\""
done

# === Images ===

create_directory "$IMAGES_DIR"

for image in $IMAGES; do
	download_image "$image" "$IMAGES_DIR"
done

# --- Clean up ---
if [ ${#INSTALLED_PACKAGES[@]} -gt 0 ]; then
	for package in "${INSTALLED_PACKAGES[@]}"; do
		remove_package "$package"
	done
fi

echol "$(basename $0) finished"
