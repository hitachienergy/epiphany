#!/bin/bash

set -euo pipefail


if [[ "$EUID" -ne 0 ]]; then
  echo "err: this script must be run as root"
  exit
fi

# beautify input path - remove double slashes if occurs
dst_dir=$(readlink -m $1)

script_path="$( cd "$(dirname "$0")" ; pwd -P )"
input_file="${script_path}/requirements.txt"
deplist="${script_path}/.dependencies"
logfile="${script_path}/log"
dst_dir_packages="${dst_dir}/packages"
dst_dir_files="${dst_dir}/files"
dst_dir_images="${dst_dir}/images"
# to download everything add "--recurse" here:
#deplist_cmd="apt-cache depends --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances --no-pre-depends"
deplist_cmd() {
    apt-cache depends --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances --no-pre-depends $1
}
download_cmd="apt-get download"



usage() {
	echo "usage: ./$(basename $0) <download_dir>"
	echo "       ./$(basename $0) /tmp/downloads"
	[[ -z "$1" ]] || exit "$1"
}

[[ $# -gt 0 ]] || usage






# some quick sanity check
echo "dependency list: ${deplist}"
echo "command used to download packages: ${download_cmd}"
echo "destination directory for packages: ${dst_dir_packages}"

## clear old dependency file
#if [[ -f "${deplist}" ]]; then
#    : > "${deplist}"
#fi

# make sure destination dir exists
mkdir -p "${dst_dir_packages}"
mkdir -p "${dst_dir_files}"
mkdir -p "${dst_dir_images}"
#if [[ ! -d "${dst_dir_packages}" ]]; then
#    mkdir -p "${dst_dir_packages}"{,packages, files, images}
#fi

. ${script_path}/add-repositories.sh 
## enable 3rd party repositories
## TODO: don't fail when dir doesn't exist or empty
## this is done in add-repositories.sh script and not needed here
#for i in "${script_path}"/repos/*; do
#    if [[ ! -f /etc/apt/sources.list.d/$(basename "${i}") ]]; then
#        echo "copying repository definition: ${i} to: /etc/apt/sources.list.d/"
#        cp "${i}" /etc/apt/sources.list.d/
#        chmod 644 "${i}"
#    else
#        echo "file /etc/apt/sources.list.d/"$(basename ${i})" already exists. make sure your repository works. skipping..."
#    fi
#done

# make sure apt knows about new repositories
apt update

# parse the input file, separete by tags: [packages], [files], [images]
packages=$(awk '/^$/ {next}; /\[packages\]/ {f=1; next}; /^\[/ {f=0}; f {print $0}' "${input_file}")
files=$(awk '/^$/ {next}; /\[files\]/ {f=1; next}; /^\[/ {f=0}; f {print $0}' "${input_file}")
images=$(awk '/^$/ {next}; /\[images\]/ {f=1; next}; /^\[/ {f=0}; f {print $0}' "${input_file}")

printf "\n" 

# clear list of cached dependencies if .dependencies is older than 15 minutes
find "$script_path" -type f -wholename "${deplist}" -mmin +15 -exec rm "${deplist}" \;
# clear list of cached dependencies if requirements.txt was recently edited
find "$script_path" -type f -wholename "$input_file" -mmin -1 -exec rm "${deplist}" \;

# PACKAGES
# if dependency list doesn't exist or is zero size then resolve dependency and store them in a deplist file
if [[ ! -f ${deplist} ]] || [[ ! -s ${deplist} ]] ; then
    # clean dependency list if process gets interrupted
    trap "rm -f ${deplist}; echo 'dependency resolution interrupted, cleaning cache file'" SIGINT SIGTERM
    echo Resolving dependencies to download. This might take a while and will be cached in ${deplist}
    while IFS= read -r package; do
        echo "package read from requirements file: $package" | tee -a ${logfile}
        # if package has a specified version e.g. "name 1.0" store it as "name=1.0*" for compatibility with "apt-get download"
        package=$(echo ${package} | awk '{if($2 != "") {print $1 "=" $2 "*"} else {print $1}}')
        echo "package to download: $package" | tee -a ${logfile}
        # store package itself in the list of dependencies...
        echo "${package}" >> "${deplist}"
        # .. and create depency list for the package
        # (names only for dependencies, no version check here, not necessary as most dependencies are backward-compatible)
	dependencies=$(deplist_cmd "${package}" | awk '/Depends/ && !/</ {print$2}' | tee -a "${deplist}")
    done <<< "${packages}"
fi

# sort and uniq dependencies
sort -u -o ${deplist} ${deplist}

# be verbose, show what will be downloaded
echo "packages to be downloaded:"
cat -n "${deplist}"

# download dependencies (supress apt-get harmless sandboxing warning when running as root)
cd $dst_dir_packages && xargs --no-run-if-empty --arg-file=${deplist} --delimiter='\n' ${download_cmd} | tee -a ${logfile} 
cd $script_path

printf "\n" 


# source common functions
. common.sh


# FILES
# process files
if [[ -z "${files}" ]]; then
    echo "no files to download"
else
    # be verbose, show what will be downloaded
    # TODO: this is the list of all files shows on every run, not only the files that will be downloaded this run
    echo "files to be downloaded:"
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
    echo "No images to download"
else
    # be verbose, show what will be downloaded
    echo "Images to be downloaded:"
    cat -n <<< "${images}"
    
    printf "\n" 
    # download images using skopeo
    while IFS= read -r image_name; do
        download_image "${image_name}" "${dst_dir_images}"
    done <<< "${images}"
fi


