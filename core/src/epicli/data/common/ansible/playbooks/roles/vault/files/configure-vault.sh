#!/bin/bash
# TODO: Revoke root token
# TODO: Policy for non-root access

HELP_MESSAGE="Usage: configure-vault.sh -c path_to_script_configuration_file -a vault_ip_address"

function print_help { echo "$HELP_MESSAGE"; }

function log_and_print {
    local STRING_TO_LOG="$1";
    echo "$STRING_TO_LOG" | tee -a configure-vault.log;
}

function fail_script {
    local STRING_TO_LOG="$1";
    log_and_print "$STRING_TO_LOG";
    exit 1;
}

function fail_on_vault_error {
    local STATUS="$1";
    local SUCCESS_MESSAGE="$2";
    local FAILURE_MESSAGE="$3";
    if [ "$1" != "1" ] ; then
        log_and_print "$SUCCESS_MESSAGE";
    else
        fail_script "$FAILURE_MESSAGE";
    fi
}

function vault_unseal {
  local INIT_FILE_PATH="$1";
  log_and_print "Unsealing vault.";
  grep -m 3 Unseal "$INIT_FILE_PATH" | awk '{print $4}' | while read -r line ; do
    vault operator unseal "$line";
    fail_on_vault_error "$?" "Unseal performed." "There was an error during unsealing of vault.";
  done
}

function enable_auditing {
    local LOG_DIR="$1";
    log_and_print "Enabling auditing.";
    vault audit list | grep "file";
    COMMAND_RESULT=(${PIPESTATUS[@]})
    if [ "$COMMAND_RESULT[0]" = "1"] ; then
        fail_script "There was an error during listing auditing.";
    fi
    if [ "$COMMAND_RESULT[1]" = "1" ] ; then
        vault audit enable file file_path="$LOG_DIR/audit.log";
        fail_on_vault_error "$?" "Auditing enabled." "There was an error during enabling auditing.";
    fi
}

function mount_secret_path {
    local SECRET_PATH="$1";
    log_and_print "Mounting secret engine.";
    vault secrets list | grep "$SECRET_PATH/";
    COMMAND_RESULT=(${PIPESTATUS[@]})
    if [ "$COMMAND_RESULT[0]" = "1" ] ; then
        fail_script "There was an error during listing secret engines.";
    fi
    if [ "$COMMAND_RESULT[1]" = "1" ] ; then
        vault secrets enable -path="$SECRET_PATH" kv-v2;
        fail_on_vault_error "$?" "Secret engine enabled under path: $SECRET_PATH." "There was an error during enabling secret engine under path: $SECRET_PATH.";
    fi
}

function integrate_kubernetes {
    log_and_print "Turning on kubernetes integration.";
    vault auth list | grep kubernetes;
    COMMAND_RESULT=(${PIPESTATUS[@]})
    if [ "$COMMAND_RESULT[0]" = "1" ] ; then
        fail_script "There was an error during listing authentication methods.";
    fi
    if [ "$COMMAND_RESULT[1]" = "1" ] ; then
        vault auth enable kubernetes;
        fail_on_vault_error "$?" "Kubernetes authentication enabled." "There was an error during enabling kubernetes authentication.";
    fi
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

INIT_FILE_PATH="$VAULT_INSTALL_PATH/init.txt"
export VAULT_ADDR="http://$VAULT_IP:8200"
PATH=$VAULT_INSTALL_PATH/bin:$PATH

trap "rm -f $HOME/.vault-token" EXIT;

if [ "${SCRIPT_AUTO_UNSEAL,,}" = "true" ] ; then
    vault_unseal "$INIT_FILE_PATH";
fi

log_and_print "Loging to vault.";
LOGIN_TOKEN="$(grep "Initial Root Token:" "$INIT_FILE_PATH" | awk -F'[ ]' '{print $4}')";
vault login -no-print "$LOGIN_TOKEN";
fail_on_vault_error "$?" "Login successful." "There was an error loging to vault.";
LOGIN_TOKEN="";

if [ "${ENABLE_AUDITING,,}" = "true" ] ; then
    enable_auditing "$LOG_DIR";
fi

mount_secret_path "$SECRET_PATH";

if [ "${KUBERNETES_INTEGRATION,,}" = "true" ] ; then
    integrate_kubernetes;
fi

exit 0;
