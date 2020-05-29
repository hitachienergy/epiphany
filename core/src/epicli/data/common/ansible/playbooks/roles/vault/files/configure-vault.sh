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
    local exit_code="$1";
    local success_message="$2";
    local failure_message="$3";
    if [ "$exit_code" != "1" ] ; then
        log_and_print "$success_message";
    else
        exit_with_error "$failure_message";
    fi
}

function initialize_vault {
    local init_file_path="$1";
    log_and_print "Checking if Vault is already initialized...";
    vault status | grep -e 'Initialized[[:space:]]*true';
    local command_result=( ${PIPESTATUS[@]} );
    if [ "${command_result[0]}" = "1" ] ; then
        exit_with_error "There was an error during checking status of Vault.";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Vault has been aldready initialized.";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Initializing vault...";
        vault operator init > $init_file_path;
        check_vault_error "$?" "Vault initialized." "There was an error during initialization of Vault.";
    fi
}

function unseal_vault {
    local init_file_path="$1";
    log_and_print "Checking if vault is already unsealed...";
    vault status | grep -e 'Sealed[[:space:]]*false';
    local command_result=( ${PIPESTATUS[@]} );
    if [ "${command_result[0]}" = "1" ] ; then
        exit_with_error "There was an error during checking status of Vault.";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Vault has been aldready usealed.";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Unsealing Vault.";
        grep --max-count=3 Unseal "$init_file_path" | awk '{print $4}' | while read -r line ; do
            vault operator unseal "$line";
            check_vault_error "$?" "Unseal performed." "There was an error during unsealing of Vault.";
        done
    fi
}

function check_if_vault_is_unsealed {
    log_and_print "Checking if vault is already unsealed...";
    vault status;
    local command_result="$?";
    if [ "$command_result" = "1" ] ; then
        exit_with_error "There was an error during checking status of Vault.";
    fi
    if [ "$command_result" = "2" ] ; then
        exit_with_error "Vault hasn't been successfully unsealed. Please configure script for auto-unseal option operator unseal Vault manually.";
    fi
}

function enable_vault_audit_logs {
    log_and_print "Checking if audit is enabled...";
    vault audit list | grep "file";
    local command_result=( ${PIPESTATUS[@]} );
    if [ "${command_result[0]}" = "1"] ; then
        exit_with_error "There was an error during listing auditing.";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Enabling auditing...";
        vault audit enable file file_path="/var/log/vault_audit.log";
        check_vault_error "$?" "Auditing enabled." "There was an error during enabling auditing.";
    fi
}

function mount_secret_path {
    local secret_path="$1";
    log_and_print "Checking if secret engine has been initialized already...";
    vault secrets list | grep "$secret_path/";
    local command_result=( ${PIPESTATUS[@]} );
    if [ "${command_result[0]}" = "1" ] ; then
        exit_with_error "There was an error during listing secret engines.";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Mounting secret engine...";
        vault secrets enable -path="$secret_path" -version=2 kv;
        check_vault_error "$?" "Secret engine enabled under path: $secret_path." "There was an error during enabling secret engine under path: $secret_path.";
    fi
}

function enable_vault_kubernetes_authentication {
    log_and_print "Checking if Kubernetes authentication has been enabled...";
    vault auth list | grep kubernetes;
    local command_result=( ${PIPESTATUS[@]} );
    if [ "${command_result[0]}" = "1" ] ; then
        exit_with_error "There was an error during listing authentication methods.";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Turning on Kubernetes authentication...";
        vault auth enable kubernetes;
        check_vault_error "$?" "Kubernetes authentication enabled." "There was an error during enabling Kubernetes authentication.";
    fi
}

function apply_epiphany_vault_policies {
    log_and_print "Applying Epiphany default Vault policies...";
    local local vault_config_data_path="$1";
    vault policy write admin $vault_config_data_path/policy-admin.hcl;
    check_vault_error "$?" "Admin policy applied." "There was an error during applying admin policy.";
    vault policy write provisioner $vault_config_data_path/policy-provisioner.hcl;
    check_vault_error "$?" "Provisioner policy applied." "There was an error during applying provisioner policy.";
}

function enable_vault_userpass_authentication {
    log_and_print "Checking if userpass authentication has been enabled...";
    vault auth list | grep userpass;
    local command_result=( ${PIPESTATUS[@]} );
    if [ "${command_result[0]}" = "1" ] ; then
        exit_with_error "There was an error during listing authentication methods.";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Turning on userpass authentication...";
        vault auth enable userpass;
        check_vault_error "$?" "Userpass authentication enabled." "There was an error during enabling userpass authentication.";
    fi
}

# TODO: Add flag to enable/disable token cleanup
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
VAULT_CONFIG_DATA_PATH="$VAULT_INSTALL_PATH/config"
export VAULT_ADDR="http://$VAULT_IP:8200"
PATH=$VAULT_INSTALL_PATH/bin:$PATH

trap cleanup EXIT INT TERM;

initialize_vault "$INIT_FILE_PATH";

if [ "${SCRIPT_AUTO_UNSEAL,,}" = "true" ] ; then
    unseal_vault "$INIT_FILE_PATH";
fi

check_if_vault_is_unsealed;

log_and_print "Logging into Vault.";
LOGIN_TOKEN="$(grep "Initial Root Token:" "$INIT_FILE_PATH" | awk -F'[ ]' '{print $4}')";
vault login -no-print "$LOGIN_TOKEN";
check_vault_error "$?" "Login successful." "There was an error while logging into Vault.";
LOGIN_TOKEN="";

if [ "${ENABLE_AUDITING,,}" = "true" ] ; then
    enable_vault_audit_logs;
fi

mount_secret_path "$SECRET_PATH";

if [ "${KUBERNETES_INTEGRATION,,}" = "true" ]  || [ "${ENABLE_VAULT_KUBERNETES_AUTHENTICATION,,}" = "true" ] ; then
    enable_vault_kubernetes_authentication;
fi

apply_epiphany_vault_policies $VAULT_CONFIG_DATA_PATH;
enable_vault_userpass_authentication;
