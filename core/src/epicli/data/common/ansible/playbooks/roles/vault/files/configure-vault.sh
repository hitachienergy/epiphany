#!/bin/bash
# Description: This script perform configuration of Hashicorp Vault to be used with Epiphany
# More information you can find in Epiphany documentation in HOWTO.md
# TODO: Revoke root token
# TODO: Policy for non-root access

HELP_MESSAGE="Usage: configure-vault.sh -c path_to_script_configuration_file -a vault_ip_address"

function print_help { echo "$HELP_MESSAGE"; }

function log_and_print {
    local string_to_log="$1";
    echo "$string_to_log" | tee -a configure-vault.log;
}

function fail_script {
    local string_to_log="$1";
    log_and_print "$string_to_log";
    exit 1;
}

function check_vault_error {
    local status="$1";
    local success_message="$2";
    local failure_message="$3";
    if [ "$status" != "1" ] ; then
        log_and_print "$success_message";
    else
        fail_script "$failure_message";
    fi
}

function unseal_vault {
  local init_file_path="$1";
  log_and_print "Unsealing Vault.";
  grep -m 3 Unseal "$init_file_path" | awk '{print $4}' | while read -r line ; do
    vault operator unseal "$line";
    check_vault_error "$?" "Unseal performed." "There was an error during unsealing of Vault.";
  done
}

function enable_auditing {
    local log_dir="$1";
    log_and_print "Enabling auditing.";
    vault audit list | grep "file";
    local COMMAND_RESULT=(${PIPESTATUS[@]})
    if [ "$COMMAND_RESULT[0]" = "1"] ; then
        fail_script "There was an error during listing auditing.";
    fi
    if [ "$COMMAND_RESULT[1]" = "1" ] ; then
        vault audit enable file file_path="$log_dir/audit.log";
        check_vault_error "$?" "Auditing enabled." "There was an error during enabling auditing.";
    fi
}

function mount_secret_path {
    local secret_path="$1";
    log_and_print "Mounting secret engine...";
    vault secrets list | grep "$secret_path/";
    local COMMAND_RESULT=(${PIPESTATUS[@]})
    if [ "$COMMAND_RESULT[0]" = "1" ] ; then
        fail_script "There was an error during listing secret engines.";
    fi
    if [ "$COMMAND_RESULT[1]" = "1" ] ; then
        vault secrets enable -path="$secret_path" -version=2 kv;
        check_vault_error "$?" "Secret engine enabled under path: $secret_path." "There was an error during enabling secret engine under path: $secret_path.";
    fi
}

function integrate_with_kubernetes {
    log_and_print "Turning on kubernetes integration.";
    vault auth list | grep kubernetes;
    local COMMAND_RESULT=(${PIPESTATUS[@]})
    if [ "$COMMAND_RESULT[0]" = "1" ] ; then
        fail_script "There was an error during listing authentication methods.";
    fi
    if [ "$COMMAND_RESULT[1]" = "1" ] ; then
        vault auth enable kubernetes;
        check_vault_error "$?" "Kubernetes authentication enabled." "There was an error during enabling kubernetes authentication.";
    fi
}

function cleanup {
    [ -e "$HOME/.vault-token" ] && rm -f "$HOME/.vault-token";
}

while getopts ":p:a:c:h?" opt; do
    case "$opt" in
        a) VAULT_IP=$OPTARG;;
        c) CONFIG_FILE=$OPTARG;;
        ? | h | *) print_help; exit 2;;
    esac
done

if [ $OPTIND -eq 1 ]; then
    print_help;
    fail_script "No options passed to script. Aborting.";
fi

. "$CONFIG_FILE";

init_file_path="$VAULT_INSTALL_PATH/init.txt"
export VAULT_ADDR="http://$VAULT_IP:8200"
PATH=$VAULT_INSTALL_PATH/bin:$PATH

trap cleanup EXIT;
trap cleanup INT;
trap cleanup TERM;

if [ "${SCRIPT_AUTO_UNSEAL,,}" = "true" ] ; then
    unseal_vault "$init_file_path";
fi

log_and_print "Logging into Vault.";
LOGIN_TOKEN="$(grep "Initial Root Token:" "$init_file_path" | awk -F'[ ]' '{print $4}')";
vault login -no-print "$LOGIN_TOKEN";
check_vault_error "$?" "Login successful." "There was an error loging into Vault.";
LOGIN_TOKEN="";

if [ "${ENABLE_AUDITING,,}" = "true" ] ; then
    enable_auditing "$log_dir";
fi

mount_secret_path "$secret_path";

if [ "${KUBERNETES_INTEGRATION,,}" = "true" ] ; then
    integrate_with_kubernetes;
fi

exit 0;
