#!/bin/bash
# this file is just a bunch of functions meant to be called from other scripts


usage() {
	echo "usage:         ./$(basename "$0") <downloads_dir>"
	echo "example:       ./$(basename "$0") /tmp/downloads"
	exit 1
}

echol() {
	echo -e "$1" | tee --append "$logfile"
}

exit_with_error() {
	echol "ERROR: $1"
	exit 1
}

# params: <file_path>
remove_file() {
	local file_path="$1"

	echol "Removing file: $file_path"
	rm -f "$file_path" || exit_with_error "Command failed: rm -f \"$file_path\""
}

# params: <dir_path>
create_directory() {
	local dir_path="$1"

	if [[ ! -d  "$dir_path" ]]; then
		mkdir -p $dir_path
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
	local dst_image="${dest_dir}/${repo_basename}-${tag}.tar"
	local retries=3

	if [[ -f ${dst_image} ]]; then
		echo "Image: "${dst_image}" already exists. Skipping..."
	else
		local tmp_file=$(mktemp)
		echo "Downloading image: $1"
		echo "Crane command is: ${crane_bin} pull --insecure --format=legacy ${image_name} ${dst_image}"
		# use temporary file for downloading to be safe from sudden interruptions (network, ctrl+c)
		run_cmd_with_retries $retries ${crane_bin} pull --insecure --platform=${docker_platform} --format=legacy ${image_name} ${tmp_file} && chmod 644 ${tmp_file} && mv ${tmp_file} ${dst_image}
	fi
}

# params: <file_url> <dest_dir> [new_filename]
download_file() {
	local file_url="$1"
	local dest_dir="$2"
	if [[ ${3-} ]]; then
		local new_filename="$3"
	fi

	local file_name
	file_name=$(basename "$file_url")
	local dest_path="${dest_dir}/${file_name}"
	local retries=3

	# wget with --timestamping sometimes failes on AWS with ERROR 403: Forbidden
	# so we remove existing file to overwrite it

	# remove old files to force redownload after a while
	# just a precaution so --continue won't append and corrupt files localy if file is updated on server without name change
	if [[ -f $dest_path && $(find "$dest_path" -mmin +60 -print) ]]; then
	    echol "File $dest_path older than 1h, redownloading..."
	    remove_file "$dest_path"
	fi

	# --no-use-server-timestamps - we don't use --timestamping and we need to expire files somehow 
	# --continue - don't download the same file multiple times, gracefully skip if file is fully downloaded	
	if [[ ${new_filename-} ]]; then
		echol "Downloading file: $file_url as $new_filename"
		run_cmd_with_retries $retries wget --no-use-server-timestamps --continue --show-progress --prefer-family=IPv4 "${file_url}" -O "${dest_dir}/${new_filename}"
	else
		echol "Downloading file: $file_url"
		run_cmd_with_retries $retries wget --no-use-server-timestamps --continue --show-progress --prefer-family=IPv4 --directory-prefix="${dest_dir}" "${file_url}"
	fi
}

# to download everything, add "--recurse" flag but then you will get much more packages (e.g. 596 vs 319)
deplist_cmd() {
    apt-cache depends --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances --no-pre-depends $1
}

get_shell_escaped_array() {
    if (( $# > 0 )); then
      printf '%q\n' "$@"
    fi
}

print_array_as_shell_escaped_string() {
    local output=$(get_shell_escaped_array "$@")
    local -a escaped=()
    if [ -n "$output" ]; then
      readarray -t escaped <<< "$output"
    fi
    if (( ${#escaped[@]} > 0 )); then
      printf '%s\n' "${escaped[*]}"
    fi
}

run_cmd() {
    local -a cmd_arr=("$@")
    local output=$(print_array_as_shell_escaped_string "${cmd_arr[@]}")
    echo "Running command:" "$output"
    "${cmd_arr[@]}"
}

run_cmd_with_retries() {
    local retries=${1}
    shift
    local -a cmd_arr=("$@")
    ( # sub-shell is used to limit scope for 'set +e'
      set +e
      trap - ERR  # disable global trap locally
      for ((i=0; i <= retries; i++)); do
        run_cmd "${cmd_arr[@]}"
        return_code=$?
        if (( return_code == 0 )); then
          break
        elif (( i < retries )); then
          sleep 1
          echo "retrying ($(( i+1 ))/${retries})"
        else
          echo "ERROR: all attempts failed"
        fi
      done
      return $return_code
    )
}
