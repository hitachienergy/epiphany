#!/usr/bin/env bash

# VERSION 1.0.5

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
		local -a gpg_key_urls
		IFS=" " read -r -a gpg_key_urls \
			<<< "$(grep -i --only-matching --perl-regexp '(?<=^gpgkey=)http[^#\n]+' <<< "$config_file_content")"
		if (( ${#gpg_key_urls[@]} > 0 )); then
			import_repo_gpg_keys "${gpg_key_urls[@]}" 3
		fi
		# to accept import of repo's GPG key (for repo_gpgcheck=1)
		yum -y repolist > /dev/null || exit_with_error "Command failed: yum -y repolist"
	fi
}

# params: <script_url>
add_repo_from_script() {
	local script_url="$1"

	echol "Running: curl $script_url | bash"
	curl "$script_url" | bash
}

# params: <backup_file_path> <path_1_to_backup1> ... [path_N_to_backup]
backup_files() {
	local backup_file_path="$1"
	shift
	local paths_to_backup=("$@")

	# --directory='/' is for tar --verify
	tar --create --verbose --verify --directory="/" --file="$backup_file_path" "${paths_to_backup[@]}"
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

# params: <file_url> <dest_dir> [new_filename]
download_file() {
	local file_url="$1"
	local dest_dir="$2"

	if [[ ${3-} ]]; then
		local file_name=$3
	else
		local file_name
		file_name=$(basename "$file_url")
	fi

	local dest_path="${dest_dir}/${file_name}"
	local retries=3

	if [[ ${3-} ]]; then
		echol "Downloading file: $file_url as $file_name"
		run_cmd_with_retries wget --quiet --directory-prefix="$dest_dir" "$file_url" -O "$dest_path" $retries || \
		exit_with_error "Command failed: wget --no-verbose --directory-prefix=$dest_dir $file_url $retries"
	else
		echol "Downloading file: $file_url"
		run_cmd_with_retries wget --quiet --directory-prefix="$dest_dir" "$file_url" $retries ||	\
		exit_with_error "Command failed: wget --no-verbose --directory-prefix=$dest_dir $file_url $retries"
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
	local dest_path="${dest_dir}/${repo_basename}-${tag}.tar"
	local retries=3

	if [[ -f $dest_path ]]; then
		echol "Image file: $dest_path already exists. Skipping..."
	else
		# use temporary file for downloading to be safe from sudden interruptions (network, ctrl+c)
		local tmp_file_path=$(mktemp)
		local crane_cmd="$CRANE_BIN  pull --insecure --platform=${DOCKER_PLATFORM} --format=legacy ${image_name} ${tmp_file_path}"
		echol "Downloading image: $image"
		{ run_cmd_with_retries $crane_cmd $retries && chmod 644 $tmp_file_path && mv $tmp_file_path $dest_path; } ||
		exit_with_error "crane failed, command was: $crane_cmd && chmod 644 $tmp_file_path && mv $tmp_file_path $dest_path"
	fi
}

# params: <dest_dir> <package_1> ... [package_N]
download_packages() {
	local dest_dir="$1"
	shift
	local packages="$@"
	local retries=3

	if [[ -n $packages ]]; then
		# when using --archlist=x86_64 yumdownloader (yum-utils-1.1.31-52) also downloads i686 packages
		run_cmd_with_retries yumdownloader --quiet --archlist="$ARCH" --exclude='*i686' --destdir="$dest_dir" $packages $retries
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

# params: <result_var> <package>
get_package_dependencies_with_arch() {
	# $1 reserved for result
	local package="$2"

	local query_output=$(repoquery --requires --resolve --queryformat '%{name}.%{arch}' --archlist=$ARCH,noarch "$package") ||
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

	local query_output=$(repoquery --queryformat '%{ui_nevra}' --archlist=$ARCH,noarch "$package") ||
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

	if [[ $group_name == "files" ]]; then
		local requirements_from_group=$(awk "/^$/ {next}; /\[${group_name}\]/ {f=1; f=2; next}; /^\[/ {f=0}; f {print \$0}" <<< "$all_requirements") ||
			exit_with_error "Function get_requirements_from_group failed for group: $group_name"
	else
		local requirements_from_group=$(awk "/^$/ {next}; /\[${group_name}\]/ {f=1; next}; /^\[/ {f=0}; f {print \$0}" <<< "$all_requirements") ||
			exit_with_error "Function get_requirements_from_group failed for group: $group_name"
	fi

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

# params: <url(s)> <retries>
import_repo_gpg_keys() {
	local retries=${!#} # get last arg
	local urls=( "${@:1:$# - 1}" )  # remove last arg

	for url in "${urls[@]}"; do
		run_cmd_with_retries rpm --import "$url" "$retries"
	done
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

remove_yum_cache_for_untracked_repos() {
	local basearch releasever
	basearch=$(uname --machine)
	releasever=$(rpm -q --provides "$(rpm -q --whatprovides 'system-release(releasever)')" | grep "system-release(releasever)" | cut -d ' ' -f 3)
	local cachedir find_output
	cachedir=$(grep --only-matching --perl-regexp '(?<=^cachedir=)[^#\n]+' /etc/yum.conf)
	cachedir="${cachedir/\$basearch/$basearch}"
	cachedir="${cachedir/\$releasever/$releasever}"
	find_output=$(find "$cachedir" -mindepth 1 -maxdepth 1 -type d -exec basename '{}' ';')
	local -a repos_with_cache=()
	if [ -n "$find_output" ]; then
		readarray -t repos_with_cache <<< "$find_output"
	fi
	local all_repos_output
	all_repos_output=$(yum repolist -v all | grep --only-matching --perl-regexp '(?<=^Repo-id)[^/]+' | sed -e 's/^[[:space:]:]*//')
	local -a all_repos=()
	readarray -t all_repos <<< "$all_repos_output"
	if (( ${#repos_with_cache[@]} > 0 )); then
		for cached_repo in "${repos_with_cache[@]}"; do
			if ! _in_array "$cached_repo" "${all_repos[@]}"; then
				run_cmd rm -rf "$cachedir/$cached_repo"
			fi
		done
	fi
}

# Runs command as array with printing it, doesn't support commands with shell operators (such as pipe or redirection)
# params: <command to execute> [--no-exit-on-error]
run_cmd() {
	local cmd_arr=("$@")

	local exit_on_error=1
	if [[ ${cmd_arr[-1]} == '--no-exit-on-error' ]]; then
		exit_on_error=0
		cmd_arr=( "${cmd_arr[@]:0:$# - 1}" )  # remove last item
	fi

	local escaped_string return_code
	escaped_string=$(_print_array_as_shell_escaped_string "${cmd_arr[@]}")
	echol "Executing: ${escaped_string}"
	"${cmd_arr[@]}"; return_code=$?
	if (( return_code != 0 )) && (( exit_on_error )); then
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
	set -- "${@:1:$#-1}"  # set new "$@"

	local cmd_arr=("$@")
	( # sub-shell is used to limit scope for 'set +e'
		set +e
		trap - ERR  # disable global trap locally
		for ((i=0; i <= retries; i++)); do
			run_cmd "${cmd_arr[@]}" '--no-exit-on-error'
			return_code=$?
			if (( return_code == 0 )); then
				break
			elif (( i < retries )); then
				sleep 1
				echol "retrying ($(( i+1 ))/${retries})"
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

usage() {
	echo "usage:         ./$(basename $0) <downloads_dir> [--no-logfile]"
	echo "example:       ./$(basename $0) /tmp/downloads"
	exit 1
}

validate_bash_version() {
	local major_version=${BASH_VERSINFO[0]}
	local minor_version=${BASH_VERSINFO[1]}
	local required_version=(4 2)  # (minor major)
	if (( major_version < ${required_version[0]} )) || (( minor_version < ${required_version[1]} )); then
		exit_with_error "This script requires Bash version ${required_version[0]}.${required_version[1]} or higher."
	fi
}

# === Helper functions (in alphabetical order) ===

_get_shell_escaped_array() {
	if (( $# > 0 )); then
		printf '%q\n' "$@"
	fi
}

# params: <value to test> <array>
_in_array() {
	local value=${1}
	shift
	local array=( "$@" )

	(( ${#array[@]} > 0 )) && printf '%s\n' "${array[@]}" | grep -q -Fx "$value"
}

# Prints string in format that can be reused as shell input (escapes non-printable characters)
_print_array_as_shell_escaped_string() {
	local output
	output=$(_get_shell_escaped_array "$@")
	local escaped=()
	if [ -n "$output" ]; then
		readarray -t escaped <<< "$output"
	fi
	if (( ${#escaped[@]} > 0 )); then
		printf '%s\n' "${escaped[*]}"
	fi
}

# === Start ===

validate_bash_version

if [[ $# -lt 1 ]]; then
	usage >&2
fi

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
readonly FILES_DIR="${DOWNLOADS_DIR}/files"
readonly PACKAGES_DIR="${DOWNLOADS_DIR}/packages"
readonly IMAGES_DIR="${DOWNLOADS_DIR}/images"
readonly REPO_PREREQ_PACKAGES_DIR="${PACKAGES_DIR}/repo-prereqs"
readonly SCRIPT_DIR="$(dirname $(readlink -f $0))" # want absolute path

# files
readonly SCRIPT_FILE_NAME=$(basename "$0")
readonly LOG_FILE_NAME="${SCRIPT_FILE_NAME}.log"
readonly LOG_FILE_PATH="${SCRIPT_DIR}/${LOG_FILE_NAME}"
readonly YUM_CONFIG_BACKUP_FILE_PATH="${SCRIPT_DIR}/${SCRIPT_FILE_NAME}-yum-repos-backup-tmp-do-not-remove.tar"
readonly CRANE_BIN="${SCRIPT_DIR}/crane"
readonly INSTALLED_PACKAGES_FILE_PATH="${SCRIPT_DIR}/${SCRIPT_FILE_NAME}-installed-packages-list-do-not-remove.tmp"
readonly PID_FILE_PATH="/var/run/${SCRIPT_FILE_NAME}.pid"
readonly ADD_MULTIARCH_REPOSITORIES_SCRIPT="${SCRIPT_DIR}/add-repositories.multiarch.sh"

#arch
readonly ARCH=$(uname -m)
echol "Detected arch: ${ARCH}"
readonly REQUIREMENTS_FILE_PATH="${SCRIPT_DIR}/requirements.${ARCH}.txt"
readonly ADD_ARCH_REPOSITORIES_SCRIPT="${SCRIPT_DIR}/add-repositories.${ARCH}.sh"
case $ARCH in
x86_64)
	readonly DOCKER_PLATFORM="linux/amd64"
	;;

aarch64)
	readonly DOCKER_PLATFORM="linux/arm64"
	;;

*)
	exit_with_error "Arch ${ARCH} unsupported"
	;;
esac
echol "Docker platform: ${DOCKER_PLATFORM}"

# --- Checks ---

[ $EUID -eq 0 ] || { echo "You have to run as root" && exit 1; }

[[ -f $REQUIREMENTS_FILE_PATH ]] || exit_with_error "File not found: $REQUIREMENTS_FILE_PATH"

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
get_requirements_from_group 'CRANE'                'crane'                 "$REQUIREMENTS_FILE_PATH"
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
for package in 'yum-utils' 'wget' 'curl' 'tar'; do
	if ! is_package_installed "$package"; then
		install_package "$package"
	fi
done

# --- Download and setup Crane for downloading images ---

if [[ -z "${CRANE}" ]] || [ $(wc -l <<< "${CRANE}") -ne 1 ] ; then
    exit_with_error "Crane binary download path undefined or more than one download path defined"
else
	if [[ -x $CRANE_BIN ]]; then
        echol "Crane binary already exists"
	else
		file_url=$(head -n 1 <<< "${CRANE}")
		echol "Downloading crane from: ${file_url}"
		download_file "${file_url}" "${SCRIPT_DIR}"
		tar_path="${SCRIPT_DIR}/${file_url##*/}"
		echol "Unpacking crane from ${tar_path} to ${CRANE_BIN}"
		run_cmd tar -xzf "${tar_path}" --directory "${SCRIPT_DIR}" "crane" --overwrite
		[[ -x "${CRANE_BIN}" ]] || run_cmd chmod +x "${CRANE_BIN}"
		remove_file "${tar_path}"
	fi
fi

# --- Enable CentOS repos ---

# -> CentOS-7 - Extras # for container-selinux and centos-release-scl packages
enable_repo 'extras'
# -> CentOS-7 - Base # for python dependencies
enable_repo 'base'

# --- Add repos ---

# noarch repositories
. ${ADD_MULTIARCH_REPOSITORIES_SCRIPT}

# arch specific repositories
. ${ADD_ARCH_REPOSITORIES_SCRIPT}
# -> Software Collections (SCL) https://wiki.centos.org/AdditionalResources/Repositories/SCL
if ! is_package_installed 'centos-release-scl'; then
	# from extras repo
	install_package 'centos-release-scl-rh'
	install_package 'centos-release-scl'
fi

# some packages are from EPEL repo
if ! is_package_installed 'epel-release'; then
	install_package 'https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm' 'epel-release'
fi

# clean metadata for upgrades (when the same package can be downloaded from changed repo)
run_cmd remove_yum_cache_for_untracked_repos

run_cmd_with_retries yum -y makecache fast 3

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
		--strip-components=2 'etc/yum.repos.d/*.repo'; then
	echol "Restored: yum repositories"
else
	exit_with_error "Extracting tar failed: $YUM_CONFIG_BACKUP_FILE_PATH"
fi

# === Files ===

create_directory "$FILES_DIR"

if [[ -z "$FILES" ]]; then
    echol "No files to download"
else
    # list of all files that will be downloaded
    echol "Files to be downloaded:"
    cat -n <<< "${FILES}"

    printf "\n"

    while IFS=' ' read -r url new_filename; do
        # download files, skip if exists, check if new filename is provided
        if [[ -z $new_filename ]]; then
            download_file "$url" "$FILES_DIR"
        elif [[ $new_filename = *" "* ]]; then
            echol "ERROR: wrong new filename for file: "
            echol "$url"
        else
            download_file "$url" "$FILES_DIR" "$new_filename"
        fi
    done <<< "$FILES"
fi

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

echol "$SCRIPT_FILE_NAME finished, execution time: $(date -u -d @$((END_TIME-START_TIME)) +'%Hh:%Mm:%Ss')"
