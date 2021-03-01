# this file is just a bunch of functions meant to be called from other scripts


usage() {
	echo "usage: ./$(basename $0) <download_dir>"
	echo "       ./$(basename $0) /tmp/downloads"
	[ -z "$1" ] || exit "$1"
}

echol() {
	echo -e "$1" | tee --append $logfile
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
# todo: skip on existing (maybe when checksum is correct?)
download_image() {
	local image_name="$1"
	local dest_dir="$2"

	local splited_image=(${image_name//:/ })
	local repository=${splited_image[0]}
	local tag=${splited_image[1]}
	local repo_basename=$(basename -- "$repository")
	local dst_image="${dest_dir}/${repo_basename}-${tag}.tar"

	#[[ ! -f $dst_image ]] || remove_file "$dst_image"
	if [[ -f ${dst_image} ]]; then
		echo "Image: "${dst_image}" already exists. Skipping..."
	else
		local tmp_file=$(mktemp)
		echo "Downloading image: $1"
		echo "Crane command is: ./crane_x86_64 pull --insecure --format=legacy ${image_name} ${dst_image}"
		# use temporary file for downloading to be safe from sudden interruptions (network, ctrl+c)
		./crane_x86_64 pull --insecure --format=legacy ${image_name} ${tmp_file} && chmod 644 ${tmp_file} && mv ${tmp_file} ${dst_image}
	fi
}

# params: <file_url> <dest_dir>
download_file() {
	local file_url="$1"
	local dest_dir="$2"

	local file_name=$(basename "$file_url")
	local dest_path="$dest_dir/$file_name"

	# wget with --timestamping sometimes failes on AWS with ERROR 403: Forbidden
	# so we remove existing file to overwrite it

	# remove old files to force redownload after a while
	# just a precaution so --continue won't append and corrupt files localy if file is updated on server without name change
	if [[ $(find ${dest_path} -mmin +60 -print) ]]; then
	    echol "File ${dest_path} older than 1h, redownloading..."
	    remove_file "$dest_path"
	fi

	echol "Downloading file: $file"

	# --no-use-server-timestamps - we don't use --timestamping and we need to expire files somehow 
	# --continue - don't download the same file multiple times, gracefully skip if file is fully downloaded	
	wget --no-use-server-timestamps --continue --show-progress --prefer-family=IPv4 --directory-prefix="${dest_dir}" "${file_url}"
}
