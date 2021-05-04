#!/bin/bash

set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

if [[ $# -lt 1 ]]; then
  usage
  exit
fi

script_path="$( cd "$(dirname "$0")" ; pwd -P )"
dst_dir=$(readlink -m $1) # beautify input path - remove double slashes if occurs
dst_dir_packages="${dst_dir}/packages"
dst_dir_files="${dst_dir}/files"
dst_dir_images="${dst_dir}/images"
deplist="${script_path}/.dependencies"
logfile="${script_path}/log"
retries="3"
download_cmd="run_cmd_with_retries $retries apt-get download"
add_repos="${script_path}/add-repositories.sh"
crane_bin="${script_path}/crane"

# source common functions
. "${script_path}/common.sh"

# arch
arch=$(uname -m)
echol "Detected arch: ${arch}"
input_file="${script_path}/requirements.${arch}.txt"
case $arch in
x86_64)
	docker_platform="linux/amd64"
	;;

*)
	exit_with_error "Arch ${arch} unsupported"
	;;
esac
echol "Docker platform: ${docker_platform}"

# checks

[ $EUID -eq 0 ] || { echo "You have to run as root"; exit 1; }

[[ -f $input_file ]] || exit_with_error "File not found: $input_file"

repos_backup_file="/tmp/epi-repository-setup-scripts/enable-system-repos.sh"
# restore system repositories in case they're missing if ansible role gets interrupted
if [[ ! -f /etc/apt/sources.list ]]; then
    if [[ -f /var/tmp/enabled-system-repos.tar ]] && [[ -f ${repos_backup_file} ]]; then
        echol "OS repositories seems missing, restoring..."
        ${repos_backup_file}
    else
        echol "/etc/apt/sources.list seems missing, you either know what you're doing or you need to fix your repositories"
    fi
fi

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
# TODO: See if we need to split this up to support different architectures
. ${add_repos}

# parse the input file, separete by tags: [crane], [packages], [files], [images]
crane=$(awk '/^$/ || /^#/ {next}; /\[crane\]/ {f=1; next}; /^\[/ {f=0}; f {print $0}' "${input_file}")
packages=$(awk '/^$/ || /^#/ {next}; /\[packages\]/ {f=1; next}; /^\[/ {f=0}; f {print $0}' "${input_file}")
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
    file_url=$(head -n 1 <<< "${crane}")
    echol "Downloading crane from: ${file_url}"
    download_file "${file_url}" "${script_path}"
    tar_path="${script_path}/${file_url##*/}"
    echol "Unpacking crane from ${tar_path} to ${crane_bin}"
    tar -xzf "${tar_path}" --directory ${script_path} "crane" --overwrite
    chmod +x "${crane_bin}"
    remove_file "${tar_path}"
    [[ -f $crane_bin ]] || exit_with_error "File not found: $crane_bin"
    [[ -x $crane_bin ]] || exit_with_error "$crane_bin has to be executable"
fi

printf "\n"

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

# be verbose, show what will be downloaded
echol "Packages to be downloaded:"
cat -n "${deplist}"

# download dependencies (apt-get sandboxing warning when running as root are harmless)
cd $dst_dir_packages && xargs --no-run-if-empty --arg-file=${deplist} --delimiter='\n' -I{} bash -c ". ${script_path}/common.sh && ${download_cmd} {}" | tee -a ${logfile}
cd $script_path

printf "\n"

# FILES
# process files
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
