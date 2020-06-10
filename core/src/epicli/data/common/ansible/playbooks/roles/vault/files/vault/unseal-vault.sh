#!/usr/bin/env bash
function log_and_print {
    local string_to_log="$1";
    echo "$(date +"%Y-%m-%d-%H:%M:%S") - $string_to_log" | tee -a /opt/vault/logs/unseal_vault.log;
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
        exit_with_error "$failure_message. Exit status: $exit_code";
    fi
}

function check_if_vault_initialized {
    vault status | grep -e 'Initialized[[:space:]]*true';
    local command_result=( ${PIPESTATUS[@]} );
    if [ "${command_result[0]}" = "1" ] ; then
        exit_with_error "There was an error during checking status of Vault.";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Vault has been aldready initialized.";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Vault not initialized, nothing to unseal...";
        exit 0;
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
        log_and_print "Vault has been aldready unsealed.";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Unsealing Vault.";
        grep --max-count=3 Unseal "$init_file_path" | awk '{print $4}' | while read -r line ; do
            vault operator unseal "$line";
            check_vault_error "$?" "Unseal performed." "There was an error during unsealing of Vault.";
        done
    fi
}

PATH=$VAULT_INSTALL_PATH/bin:/usr/local/bin/:$PATH;
INIT_FILE_PATH="$1";
VAULT_IP="$2";
export VAULT_ADDR="http://$VAULT_IP:8200"

count=1;
is_vault_running="false";
while [ "$count" -le 10 ] && [ "$is_vault_running" = "false" ] ; do
    log_and_print "Checking if vault is running...";
    response_code=$(curl -o -I -L -s -w "%{http_code}" "$VAULT_ADDR");
    if [ $response_code = 200 ] ; then
          is_vault_running="true";
    fi
    sleep 2;
    count=$[count + 1];
done
if [ "$is_vault_running" = "false" ] ; then
    exit 1;
fi
check_if_vault_initialized;
if [ -f "$INIT_FILE_PATH" ]; then
    unseal_vault "$INIT_FILE_PATH";
else
    exit_with_error "Init file doesn't exist. Cannot unseal.";
fi
