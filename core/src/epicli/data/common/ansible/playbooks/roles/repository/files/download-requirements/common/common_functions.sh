last_error=''  # holds last occurred error msg


echol() {
#
# Print to stdout, optionally to a log file.
# Requires $CREATE_LOGFILE and $LOG_FILE_PATH to be defined.
#
# :param $@: args to be printed
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


__at_least_one_test_pass() {
#
# Iterate over all arguments each time call test $function and check result.
# If at least one call passes, function will yield success.
#
# :param $1: test function
# :param $@: arguments to be tested
# :return: 0 - success, 1 - failure
    local function=$1
    shift

    local args=$@
    local total_count=$#
    local failed_count=0

    for arg in $args; do
        echol "- $arg..."
        $function $arg

        (( $? == 0 )) && return 0

        failed_count=$(( $failed_count + 1 ))
    done

    (( $total_count != $failed_count )) || return 1
    return 0
}


__test_address_curl() {
#
# Test address connection without downloading any resource.
#
# :param $1: url to be tested
# :return: curl exit value
#
    last_error=$(curl --show-error --silent $1 2>&1 >/dev/null)
    return $?
}


__check_curl() {
#
# Use curl in silent mode to check if target `url` is available.
#
# :param $@: urls to be tested
# :return: 0 - success, 1 - failure
#
    echol "Testing curl connection:"

    (( $# > 0 )) || exit_with_error "_check_curl: no url provided"

    __at_least_one_test_pass __test_address_curl $@
}


__test_address_wget() {
#
# Test address connection without downloading any resource.
#
# :param $1: url to be tested
# :return: wget exit value
#
    last_error=$(wget --spider $1 2>&1 >/dev/null)
    return $?
}


__check_wget() {
#
# Use wget in spider mode (without downloading resources) to check if target `url`
# is available.
#
# :param $@: urls to be tested
# :return: 0 - success, 1 - failure
#
    echol "Testing wget connection:"

    (( $# > 0 )) || exit_with_error "_check_wget: no url provided"

    __at_least_one_test_pass __test_address_wget $@
}


__test_apt_repo() {
#
# Update a single repository.
#
# :param $1: repository to be updated
# :return: apt return value
#
    last_error=$(apt update -o Dir::Etc::sourcelist=$1 2>&1 >/dev/null)
    local ret_val=$?

    (( $ret_val == 0 )) || return $ret_val

    # make sure that there were no error messages:
    [[ -z $(echo "$last_error" | tr '[:upper:]' '[:lower:]' | grep 'err\|fail') ]] || return 1

    return 0
}


__check_apt() {
#
# Use `apt update` to make sure that there is connection to repositories.
#
# :param $@: repos to be tested
# :return: 0 - success, 1 - failure
#
    echol "Testing apt connection:"

    (( $# > 0 )) || exit_with_error "_check_apt: no repositories provided"
    local repos=$@

    (( $UID == 0 )) || exit_with_error "apt needs to be run as a root"

    __at_least_one_test_pass __test_apt_repo $repos
    return $?
}


__test_yum_repo() {
#
# List packages from a single repository.
#
# :param $1: repository to be listed
# :return: yum return value
#
    last_error=$(yum --quiet --disablerepo=* --enablerepo=$1 list available 2>&1 >/dev/null)
    return $?
}


__check_yum() {
#
# Use `yum list` to make sure that there is connection to repositories.
# Query available packages for each repository.
#
# :param $@: repositories to be tested
# :return: 0 - success, 1 - failure
#
    echol "Testing yum connection:"

    (( $# > 0 )) || exit_with_error "_check_yum: no repositories provided"
    local repos=$@

    __at_least_one_test_pass __test_yum_repo $repos
    return $?
}


__test_crane_repo() {
#
# List packages from a single repository.
# Requires $CRANE_BIN to be defined
#
# :param $1: repository to be listed
# :return: crane return value
#
    last_error=$($CRANE_BIN ls $1 2>&1 >/dev/null)
    return $?
}


__check_crane() {
#
# Use `crane ls` to make sure that there is connection to repositories.
# Query available packages for each repository.
#
# :param $@: repositories to be tested
# :return: 0 - success, 1 - failure
#
    echol "Testing crane connection:"

    (( $# > 0 )) || exit_with_error "_check_crane: no repository provided"
    local repos=$@

    __at_least_one_test_pass __test_crane_repo $repos
    return $?
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
# :param $1: which `tool` to test
# :param $@: optional parameters used by some tools such as `url`
#
    [[ $internet_access_checks_enabled == "no" ]] && return 0

    [[ $# -lt 1 ]] && exit_with_error '"tool" argument not provided'
    local tool=$1

    shift  # discard tool variable

    [[ ! -n ${tools[$tool]} ]] && exit_with_error "no such tool: \"$tool\""

    (  # disable -e in order to handle non-zero return values
        set +e

        ${tools[$tool]} $@

        if (( $? == 0 )); then
            echol "Connection successful."
        else
            exit_with_error "Connection failure, reason: [$last_error]"
        fi
    )
}
