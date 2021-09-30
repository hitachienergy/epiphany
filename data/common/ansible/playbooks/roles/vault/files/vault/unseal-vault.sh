#!/usr/bin/env bash

function log_and_print {
    local string_to_log="$1";
    echo "$(date +"%Y-%m-%d-%H:%M:%S"): $string_to_log" | tee -a /opt/vault/logs/unseal_vault.log;
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
    if [ "$exit_code" == "0" ] ; then
        log_and_print "$success_message";
    else
        exit_with_error "$failure_message Exit status: $exit_code";
    fi
}

function check_if_vault_is_initialized {
    vault status -format json | grep -q '"initialized": true';
    local command_result=( "${PIPESTATUS[@]}" );
    if [ "${command_result[0]}" = "1" ] ; then
        exit_with_error "There was an error during checking status of Vault.";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Vault is initialized.";
    elif [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Vault is not initialized, nothing to unseal.";
        exit 0;
    fi
}

function unseal_vault {
    local init_file_path="$1";
    log_and_print "Checking if vault is already unsealed...";
    vault status -format json | grep -q '"sealed": false';
    local command_result=( "${PIPESTATUS[@]}" );
    if [ "${command_result[0]}" = "1" ] ; then
        exit_with_error "There was an error during checking status of Vault.";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Vault is already unsealed. Nothing to do.";
    elif [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Unsealing Vault...";
        grep --max-count=3 Unseal "$init_file_path" | awk '{print $4}' | while read -r line ; do
            vault operator unseal "$line";
            check_vault_error "$?" "Unseal performed." "There was an error during unsealing of Vault.";
        done
    fi
}

function check_if_vault_is_running {
    local vault_address="${1:?missing value}"
    local timeout="${2:?missing value}"
    local is_running="false"
    local delay=2
    while (( timeout >= 0 )) && [ "$is_running" = "false" ] ; do
        log_and_print "Checking if Vault is running..."
        response_code=$(curl -o -I -L -s -w "%{http_code}" "$vault_address/v1/sys/seal-status")
        if (( response_code == 200 )) ; then
            is_running="true"
        fi
        sleep $delay
        timeout=$((timeout - delay))
    done
    if [ "$is_running" = "false" ] ; then
        exit_with_error "Vault is not running. Please solve the problem and run the script again.";
    else
        log_and_print "Vault is running."
    fi
}

# --- Start ---

INIT_FILE_PATH="${1:?missing argument}";
VAULT_IP="${2:?missing argument}";
VAULT_PROTOCOL="${3:?missing argument}";

PATH=$VAULT_INSTALL_PATH/bin:/usr/local/bin:$PATH;
export VAULT_ADDR="$VAULT_PROTOCOL://$VAULT_IP:8200"

check_if_vault_is_running "$VAULT_ADDR" 10;
check_if_vault_is_initialized;

if [ -f "$INIT_FILE_PATH" ]; then
    unseal_vault "$INIT_FILE_PATH";
else
    exit_with_error "Init file doesn't exist. Cannot unseal.";
fi
