#!/bin/bash

set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

script_path="$( cd "$(dirname "$0")" ; pwd -P )"

# source common functions
. "${script_path}/common.sh"

internet_access_checks_enabled="yes"
CREATE_LOGFILE="yes"
LOG_FILE_PATH="${script_path}/log"

. "${script_path}/common/common_functions.sh"

if [[ $# -lt 1 ]]; then
  usage
  exit
fi

if [[ "$EUID" -ne 0 ]]; then
  echo "err: this script must be run as root"
  exit
fi

script_path="$( cd "$(dirname "$0")" ; pwd -P )"
input_file="${script_path}/requirements.txt"
dst_dir=$(readlink -m $1) # beautify input path - remove double slashes if occurs
dst_dir_packages="${dst_dir}/packages"
dst_dir_files="${dst_dir}/files"
dst_dir_images="${dst_dir}/images"
deplist="${script_path}/.dependencies"
retries="3"
download_cmd="run_cmd_with_retries $retries apt-get download"
add_repos="${script_path}/add-repositories.sh"
CRANE_BIN="${script_path}/crane"
apt_sources_list="/etc/apt/sources.list"

# to download everything, add "--recurse" flag but then you will get much more packages (e.g. 596 vs 319)
deplist_cmd() {
    apt-cache depends --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances --no-pre-depends $1
}

# source common functions
. "${script_path}/common.sh"

repos_backup_file="/tmp/epi-repository-setup-scripts/enable-system-repos.sh"
# restore system repositories in case they're missing if ansible role gets interrupted
if [[ ! -f $apt_sources_list || ! -s $apt_sources_list ]]; then
    if [[ -f /var/tmp/enabled-system-repos.tar ]] && [[ -f ${repos_backup_file} ]]; then
        echol "OS repositories seems missing, restoring..."
        ${repos_backup_file}
    else
        echol "$apt_sources_list seems missing or is empty, you either know what you're doing or you need to fix your repositories"
    fi
fi

check_connection apt $apt_sources_list

# install prerequisites which might be missing
apt install -y wget gpg curl tar

# some quick sanity check
echol "Dependency list: ${deplist}"
echol "Command used to download packages: ${download_cmd}"
echol "Destination directory for packages: ${dst_dir_packages}"

# make sure destination dir exists
mkdir -p "${dst_dir_packages}"
mkdir -p "${dst_dir_files}"
mkdir -p "${dst_dir_images}"

# mask custom repositories to avoid possible conflicts
shopt -s nullglob
for i in /etc/apt/sources.list.d/*.list; do
    mv "${i}" "${i}.bak"
done
shopt -u nullglob

# add 3rd party repositories
. ${add_repos}

check_connection apt $(ls /etc/apt/sources.list.d)
apt update

# parse the input file, separete by tags: [crane], [packages], [packagesfromurl], [files], [images]
crane=$(awk '/^$/ || /^#/ {next}; /\[crane\]/ {f=1; next}; /^\[/ {f=0}; f {print $0}' "${input_file}")
packages=$(awk '/^$/ || /^#/ {next}; /\[packages\]/ {f=1; next}; /^\[/ {f=0}; f {print $0}' "${input_file}")
packagesfromurl=$(awk '/^$/ || /^#/ {next}; /\[packagesfromurl\]/ {f=1; next}; /^\[/ {f=0}; f {print $0}' "${input_file}")
files=$(awk '/^$/ || /^#/ {next}; /\[files\]/ {f=1; next}; /^\[/ {f=0}; f {print $0}' "${input_file}")
images=$(awk '/^$/ || /^#/ {next}; /\[images\]/ {f=1; next}; /^\[/ {f=0}; f {print $0}' "${input_file}")

printf "\n"

# clear list of cached dependencies if .dependencies is older than 15 minutes
find "$script_path" -type f -wholename "${deplist}" -mmin +15 -exec rm "${deplist}" \;
# clear list of cached dependencies if requirements.txt was recently edited
find "$script_path" -type f -wholename "$input_file" -mmin -1 -exec rm "${deplist}" \;

# CRANE
if [[ -z "${crane}" ]] || [ $(wc -l <<< "${crane}") -ne 1 ] ; then
    exit_with_error "Crane binary download path undefined or more than one download path defined"
else
    if [[ -x $CRANE_BIN ]]; then
        echol "Crane binary already exists"
    else
        file_url=$(head -n 1 <<< "${crane}")

        check_connection wget $file_url

        echol "Downloading crane from: $file_url"
        download_file "$file_url" "$script_path"
        tar_path="${script_path}/${file_url##*/}"
        echol "Unpacking crane from $tar_path to $CRANE_BIN"
        tar -xzf "$tar_path" --directory "$script_path" "crane" --overwrite
        chmod +x "$CRANE_BIN"
        remove_file "$tar_path"
        [[ -f $CRANE_BIN ]] || exit_with_error "File not found: $CRANE_BIN"
        [[ -x $CRANE_BIN ]] || exit_with_error "$CRANE_BIN has to be executable"
    fi
fi

printf "\n"

check_connection crane $(for image in $images; do splitted=(${image//:/ }); echo "${splitted[0]}"; done)

# PACKAGES
# if dependency list doesn't exist or is zero size then resolve dependency and store them in a deplist file
if [[ ! -f ${deplist} ]] || [[ ! -s ${deplist} ]] ; then
    # clean dependency list if process gets interrupted
    trap "rm -f ${deplist}; echol 'Dependency resolution interrupted, cleaning cache file'" SIGINT SIGTERM
    echo Resolving dependencies to download. This might take a while and will be cached in ${deplist}
    while IFS= read -r package; do
        echol "Package read from requirements file: $package"
        # if package has a specified version e.g. "name 1.0" store it as "name=1.0*" for compatibility with "apt-get download"
        package=$(echo ${package} | awk '{if($2 != "") {print $1 "=" $2 "*"} else {print $1}}')
        echol "Package to download: $package"
        # store package itself in the list of dependencies...
        echol "${package}" >> "${deplist}"
        # .. and create depency list for the package
        # (names only for dependencies, no version check here, not necessary as most dependencies are backward-compatible)
        dependencies=$(deplist_cmd "${package}" | awk '/Depends/ && !/</ {print$2}' | tee -a "${deplist}")
    done <<< "${packages}"
fi

# sort and uniq dependencies
sort -u -o ${deplist} ${deplist}

if [[ -z $deplist ]]; then
    echol "No packages to be downloaded"
else
    echol "Packages to be downloaded:"
    cat -n "$deplist"

    # download dependencies (apt-get sandboxing warning when running as root are harmless)
    cd "$dst_dir_packages" && xargs --no-run-if-empty --arg-file="$deplist" --delimiter='\n' -I{} bash -c ". ${script_path}/common.sh && ${download_cmd} {}" | tee -a "${LOG_FILE_PATH}"
    cd "$script_path"
fi

printf "\n"

# PACKAGES AS URL
# process files

check_connection wget $(for file in $packagesfromurl; do echo "$file"; done)


if [[ -z "${packagesfromurl}" ]]; then
    echol "No packages from URL to download"
else
    # be verbose, show what will be downloaded
    # TODO: this is the list of all files shows on every run, not only the files that will be downloaded this run
    echol "Packages from URL to be downloaded:"
    cat -n <<< "${files}"

    printf "\n"
    # download files using wget
    while IFS= read -r file; do
        # download files, skip if exists
        #wget --no-verbose --continue --directory-prefix="${dst_dir_files}" "${file}"
        #wget --continue --show-progress --directory-prefix="${dst_dir_files}" "${file}"
        download_file "${file}" "${dst_dir_packages}"
    done <<< "${files}"
fi

# FILES
# process files

check_connection wget $(for file in $files; do echo "$file"; done)


if [[ -z "${files}" ]]; then
    echol "No files to download"
else
    # be verbose, show what will be downloaded
    # TODO: this is the list of all files shows on every run, not only the files that will be downloaded this run
    echol "Files to be downloaded:"
    cat -n <<< "${files}"

    printf "\n"
    # download files using wget
    while IFS= read -r file; do
        # download files, skip if exists
        #wget --no-verbose --continue --directory-prefix="${dst_dir_files}" "${file}"
        #wget --continue --show-progress --directory-prefix="${dst_dir_files}" "${file}"
        download_file "${file}" "${dst_dir_files}"
    done <<< "${files}"
fi

printf "\n"

# IMAGES
# process images

create_directory "${dst_dir_images}"

if [[ -z "${images}" ]]; then
    echol "No images to download"
else
    # be verbose, show what will be downloaded
    echol "Images to be downloaded:"
    cat -n <<< "${images}"

    printf "\n"
    # download images using crane
    while IFS= read -r image_name; do
        download_image "${image_name}" "${dst_dir_images}"
        if [ $? != 0 ]; then
            echo "Crane download error, retrying..."
            download_image "${image_name}" "${dst_dir_images}"
        fi
    done <<< "${images}"
fi

# CLEANUP
for i in $(grep -o '[[:blank:]]/etc/apt/sources.list.d/.*list' ${add_repos}); do
    if [[ -f ${i} ]]; then
        echol "Cleaning up 3rd party repository: rm ${i}"
        rm -f ${i}
	#TODO: remove apt keys
    fi
done

# restore masked custom repositories to their original names
shopt -s nullglob
for i in /etc/apt/sources.list.d/*.list.bak; do
    mv "${i}" "${i::-4}"
done
shopt -u nullglob
