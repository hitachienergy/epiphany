#!/bin/bash
# Description: This script configures Hashicorp Vault to be used with Epiphany
# You can find more information in Epiphany documentation in HOWTO.md
# TODO: Revoke root token
# TODO: Policy for non-root access

HELP_MESSAGE="Usage: configure-vault.sh -c SCRIPT_CONFIGURATION_FILE_PATH -a VAULT_IP_ADDRESS"

function print_help { echo "$HELP_MESSAGE"; }

function log_and_print {
    local string_to_log="$1";
    echo "$string_to_log" | tee -a configure-vault.log;
}

function exit_with_error {
    local string_to_log="$1";
    log_and_print "ERROR: $string_to_log";
    exit 1;
}

function check_vault_error {
    local exit_code ="$1";
    local success_message="$2";
    local failure_message="$3";
    if [ "$exit_code" != "1" ] ; then
        log_and_print "$success_message";
    else
        exit_with_error "$failure_message";
    fi
}

function unseal_vault {
  local init_file_path="$1";
  log_and_print "Unsealing Vault.";
  grep --max-count=3 Unseal "$init_file_path" | awk '{print $4}' | while read -r line ; do
    vault operator unseal "$line";
    check_vault_error "$?" "Unseal performed." "There was an error during unsealing of Vault.";
  done
}

function enable_vault_audit_logs {
    log_and_print "Enabling auditing.";
    vault audit list | grep "file";
    local COMMAND_RESULT=(${PIPESTATUS[@]})
    if [ "$COMMAND_RESULT[0]" = "1"] ; then
        exit_with_error "There was an error during listing auditing.";
    fi
    if [ "$COMMAND_RESULT[1]" = "1" ] ; then
        vault audit enable file file_path="/var/log/vault_audit.log";
        check_vault_error "$?" "Auditing enabled." "There was an error during enabling auditing.";
    fi
}

function mount_secret_path {
    local secret_path="$1";
    log_and_print "Mounting secret engine...";
    vault secrets list | grep "$secret_path/";
    local command_result=(${PIPESTATUS[@]})
    if [ "$command_result[0]" = "1" ] ; then
        exit_with_error "There was an error during listing secret engines.";
    fi
    if [ "$command_result[1]" = "1" ] ; then
        vault secrets enable -path="$secret_path" -version=2 kv;
        check_vault_error "$?" "Secret engine enabled under path: $secret_path." "There was an error during enabling secret engine under path: $secret_path.";
    fi
}

function integrate_with_kubernetes {
    log_and_print "Turning on Kubernetes integration.";
    vault auth list | grep kubernetes;
    local command_result=(${PIPESTATUS[@]})
    if [ "$command_result[0]" = "1" ] ; then
        exit_with_error "There was an error during listing authentication methods.";
    fi
    if [ "$command_result[1]" = "1" ] ; then
        vault auth enable kubernetes;
        check_vault_error "$?" "Kubernetes authentication enabled." "There was an error during enabling Kubernetes authentication.";
    fi
}

function cleanup {
    rm -f "$HOME/.vault-token";
}

while getopts ":a:c:h?" opt; do
    case "$opt" in
        a) VAULT_IP=$OPTARG;;
        c) CONFIG_FILE=$OPTARG;;
        ? | h | *) print_help; exit 2;;
    esac
done

if [ $OPTIND -eq 1 ]; then
    print_help;
    exit_with_error "No options passed to script. Aborting.";
fi

source "$CONFIG_FILE";

INIT_FILE_PATH="$VAULT_INSTALL_PATH/init.txt"
export VAULT_ADDR="http://$VAULT_IP:8200"
PATH=$VAULT_INSTALL_PATH/bin:$PATH

trap cleanup EXIT INT TERM;

if [ "${SCRIPT_AUTO_UNSEAL,,}" = "true" ] ; then
    unseal_vault "$INIT_FILE_PATH";
fi

log_and_print "Logging into Vault.";
LOGIN_TOKEN="$(grep "Initial Root Token:" "$INIT_FILE_PATH" | awk -F'[ ]' '{print $4}')";
vault login -no-print "$LOGIN_TOKEN";
check_vault_error "$?" "Login successful." "There was an error while logging into Vault.";
LOGIN_TOKEN="";

if [ "${ENABLE_AUDITING,,}" = "true" ] ; then
    enable_vault_audit_logs;
fi

mount_secret_path "$SECRET_PATH";

if [ "${KUBERNETES_INTEGRATION,,}" = "true" ] ; then
    integrate_with_kubernetes;
fi

exit 0;
