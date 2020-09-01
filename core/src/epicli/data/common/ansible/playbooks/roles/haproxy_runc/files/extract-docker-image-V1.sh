#!/usr/bin/env bash

: ${DEBUG:=}
: ${IMAGE_TAR:="$1"}
: ${OUTPUT_DIR:="$2"}

set -o errexit -o nounset -o pipefail

[[ -n "$DEBUG" ]] && set -x || true
[[ -n "$IMAGE_TAR" ]] && [[ -f "$IMAGE_TAR" ]]

# Assert that required binaries are available in PATH.
which basename readlink xargs dirname install tar jq find sort uniq rm cp

readonly IMAGE_NAME="$(basename "$IMAGE_TAR" .tar)"

readonly SELF="$(readlink -f "$0" | xargs dirname)"
readonly CACHE="$SELF/.cache"

readonly _IMG_="$CACHE/$IMAGE_NAME.img"
readonly _TMP_="$CACHE/$IMAGE_NAME.tmp"

if [[ -n "$OUTPUT_DIR" ]]; then
    readonly _OUT_="$OUTPUT_DIR"
else
    readonly _OUT_="$CACHE/$IMAGE_NAME.out"  # default value
fi

function extract_image {
    if [[ -d "$_IMG_/" ]]; then
        return
    fi
    install -d "$_IMG_/"
    tar xpf "$IMAGE_TAR" -C "$_IMG_/"
}

function get_layer_name {
    local layer_file="$1" layer_name
    # Handle two common layer naming convetions:
    layer_name="${layer_file%%/layer.tar}"  # docker save
    layer_name="${layer_name%%.tar}"        # skopeo copy
    echo "$layer_name"
}

function get_layer_files {
    jq -r '.[0].Layers[]' "$_IMG_/manifest.json"
}

function get_layer_names {
    local layer_file
    get_layer_files | while IFS= read layer_file; do
        get_layer_name "$layer_file"
    done
}

# Extract each layer's .tar archive into separate directories named as layers themselves.
function extract_layers {
    local layer_file
    get_layer_files | while IFS= read layer_file; do
        local layer_name="$(get_layer_name "$layer_file")"
        if [[ -d "$_TMP_/$layer_name/" ]]; then
            continue
        fi
        install -d "$_TMP_/$layer_name/"
        tar xpf "$_IMG_/$layer_file" -C "$_TMP_/$layer_name/"
    done
}

# Remove files according to "whiteouts" (https://github.com/moby/moby/blob/master/image/spec/v1.2.md#creating-an-image-filesystem-changeset).
function process_whiteouts {
    local layer_name="$1" whiteout

    (cd "$_TMP_/$layer_name/" && find . -type f -name '.wh..wh..opq') \
    | while IFS= read whiteout; do
        echo whiteout = "$whiteout"
        rm -f "$_TMP_/$layer_name/$whiteout"
    done

    (cd "$_TMP_/$layer_name/" && find . -type f -name '.wh.*') \
    | while IFS= read whiteout; do
        echo whiteout = "$whiteout"
        rm -f "$_TMP_/$layer_name/$whiteout"
        echo must_be_removed = "${whiteout/.wh./}"
        rm -rf "$_OUT_/${whiteout/.wh./}"
    done
}

# The tar and cp commands do not support replacing a file/directory with a symlink or vice versa.
# To handle it, we detect such changes beforehand and clean the output directory.
function process_symlinks {
    local layer_name="$1" must_be_removed

    (cd "$_OUT_/" && find . -type f -or -type d; cd "$_TMP_/$layer_name/" && find . -type l) | sort | uniq -d \
    | while IFS= read must_be_removed; do
        echo must_be_removed = "$must_be_removed"
        rm -rf "$_OUT_/$must_be_removed"
    done

    (cd "$_OUT_/" && find . -type l; cd "$_TMP_/$layer_name/" && find . -type f -or -type d) | sort | uniq -d \
    | while IFS= read must_be_removed; do
        echo must_be_removed = "$must_be_removed"
        rm -rf "$_OUT_/$must_be_removed"
    done

    cp --preserve --recursive --no-dereference "$_TMP_/$layer_name/." "$_OUT_/"
}

function merge_layers {
    if [[ -d "$_OUT_/" ]]; then
        return
    fi
    # Ensure output directory exists.
    install -d "$_OUT_/"

    local layer_name
    get_layer_names | while IFS= read layer_name; do
        process_whiteouts "$layer_name"
        process_symlinks "$layer_name"
    done
}

function remove_cache {
    rm -rf "$_IMG_/" "$_TMP_/"
}

function remove_all {
    rm -rf "$_OUT_/"
    remove_cache
}

function main {
    trap remove_cache EXIT
    trap remove_all ERR INT TERM
    extract_image
    extract_layers
    merge_layers
}

main

# vim:ts=4:sw=4:et:syn=sh:
