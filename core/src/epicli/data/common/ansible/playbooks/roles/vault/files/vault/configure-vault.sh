#!/usr/bin/env bash
# Description: This script configures Hashicorp Vault to be used with Epiphany
# You can find more information in Epiphany documentation in HOWTO.md
# TODO: Revoke root token
# TODO: Add configurable log paths
# TODO: Make devweb-app policy and role configurable (function integrate_with_kubernetes)
# TODO: Make Helm chart location configurable (function configure_kubernetes)

HELP_MESSAGE="Usage: configure-vault.sh -c SCRIPT_CONFIGURATION_FILE_PATH -a VAULT_IP_ADDRESS -p {http|https} -v {true|false}"

function print_help { echo "$HELP_MESSAGE"; }

function log_and_print {
    local string_to_log="$1";
    echo "$(date +"%Y-%m-%d-%H:%M:%S"): $string_to_log" | tee -a /opt/vault/logs/configure_vault.log;
}

function exit_with_error {
    local string_to_log="$1";
    log_and_print "ERROR: $string_to_log";
    exit 1;
}

function check_status {
    local exit_code="$1";
    local success_message="$2";
    local failure_message="$3";
    if [ "$exit_code" = "0" ] ; then
        log_and_print "$success_message";
    else
        exit_with_error "$failure_message Exit status: $exit_code";
    fi
}

function initialize_vault {
    local init_file_path="$1";
    log_and_print "Checking if Vault is already initialized...";
    vault status -format json | grep -q '"initialized": true';
    local command_result=( "${PIPESTATUS[@]}" );
    if [ "${command_result[0]}" = "1" ] ; then
        exit_with_error "There was an error during checking status of Vault.";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Vault is already initialized.";
    elif [ "${command_result[1]}" = "1" ] ; then
        touch "$init_file_path";
        chmod 0640 "$init_file_path";
        log_and_print "Initializing Vault...";
        vault operator init > "$init_file_path";
        check_status $? "Vault initialized." "There was an error during initialization of Vault.";
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
        log_and_print "Vault is already unsealed.";
    elif [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Unsealing Vault...";
        grep --max-count=3 Unseal "$init_file_path" | awk '{print $4}' | while read -r line ; do
            vault operator unseal "$line";
            check_status $? "Unseal performed." "There was an error during unsealing of Vault.";
        done
    fi
}

function check_if_vault_is_unsealed {
    log_and_print "Checking if vault is already unsealed...";
    vault status;
    local command_result=$?;
    if [ "$command_result" = "1" ] ; then
        exit_with_error "There was an error during checking status of Vault.";
    elif [ "$command_result" = "2" ] ; then
        exit_with_error "Vault hasn't been successfully unsealed. Please configure script for auto-unsealing or unseal Vault manually.";
    fi
}

function enable_vault_audit_logs {
    log_and_print "Checking if audit logging is enabled...";
    vault audit list | grep "file";
    local command_result=( "${PIPESTATUS[@]}" );
    if [ "${command_result[0]}" = "1" ] ; then  #IMPORTANT exit code = 2 if audit list is empty so it is ignored
        exit_with_error "There was an error during listing audit devices. Exit status: ${command_result[0]}";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Audit logging is already enabled.";
    elif [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Enabling audit logging...";
        vault audit enable file file_path="/opt/vault/logs/vault_audit.log";
        check_status $? "Audit logging enabled." "There was an error during enabling audit logging.";
    fi
}

function mount_secret_path {
    local secret_path="$1";
    log_and_print "Checking if secret engine is already initialized...";
    vault secrets list | grep "$secret_path/";
    local command_result=( "${PIPESTATUS[@]}" );
    if [ "${command_result[0]}" != "0" ] ; then
        exit_with_error "There was an error during listing secret engines. Exit status: ${command_result[0]}";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Secret engine is already mounted under path: $secret_path.";
    elif [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Mounting secret engine...";
        vault secrets enable -path="$secret_path" -version=2 kv;
        check_status $? "Secret engine enabled under path: $secret_path." "There was an error during enabling secret engine under path: $secret_path.";
    fi
}

function enable_vault_kubernetes_authentication {
    log_and_print "Checking if Kubernetes authentication is enabled...";
    vault auth list | grep kubernetes;
    local command_result=( "${PIPESTATUS[@]}" );
    if [ "${command_result[0]}" != "0" ] ; then
        exit_with_error "There was an error during listing authentication methods. Exit status: ${command_result[0]}";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Kubernetes authentication is already enabled.";
    elif [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Turning on Kubernetes authentication...";
        vault auth enable kubernetes;
        check_status $? "Kubernetes authentication enabled." "There was an error during enabling Kubernetes authentication.";
    fi
}

function kubectl_with_retries {
    local kubectl_args="$1";
    local number_of_retries="${2:-69}";  # use default value of 69
    local number_of_seconds="${3:-2}";   # use default value of 2
    local retry;

    for (( retry = 0; retry < number_of_retries; retry++ )); do
        sleep $number_of_seconds;
        if RESULT="$($SHELL -c "kubectl $kubectl_args")"; then  # please note, RESULT is a global variable!
            return 0;
        fi;
    done;

    # Return original command string for debugging purposes.
    RESULT="Command >>>> kubectl $kubectl_args <<<< failed after $retry retries.";
    return 1;
}

function integrate_with_kubernetes {
    local vault_config_data_path="$1";
    local kubernetes_namespace="$2";
    local policy_name="devweb-app";
    local role_name="devweb-app";

    log_and_print "Turning on Kubernetes integration...";

    local token_reviewer_jwt;
    if kubectl_with_retries "--kubeconfig=/etc/kubernetes/admin.conf get secret vault-auth -o go-template='{{ .data.token }}'"; then
        if ! token_reviewer_jwt="$(base64 --decode <<< "$RESULT")"; then
            exit_with_error "Unable to base64/decode vault-auth secret.";
        fi;
    else
        exit_with_error "$RESULT";
    fi;

    local kube_ca_cert;
    if kubectl_with_retries "--kubeconfig=/etc/kubernetes/admin.conf config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}'"; then
        if ! kube_ca_cert="$(base64 --decode <<< "$RESULT")"; then
            exit_with_error "Unable to base64/decode kubernetes certificate authority data."
        fi;
    else
        exit_with_error "$RESULT";
    fi;

    local kube_host;
    if kubectl_with_retries "--kubeconfig=/etc/kubernetes/admin.conf config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.server}'"; then
        kube_host="$RESULT";
    else
        exit_with_error "$RESULT";
    fi;

    vault write auth/kubernetes/config token_reviewer_jwt="$token_reviewer_jwt" kubernetes_host="$kube_host" kubernetes_ca_cert="$kube_ca_cert";
    check_status $? "Kubernetes parameters written to auth/kubernetes/config." "There was an error during writing Kubernetes parameters to auth/kubernetes/config.";

    vault policy write "$policy_name" "$vault_config_data_path/policies/policy-application.hcl";
    check_status $? "Application policy applied." "There was an error during applying application policy.";

    vault write "auth/kubernetes/role/$role_name" bound_service_account_names=internal-app bound_service_account_namespaces="$kubernetes_namespace" policies="$policy_name" ttl=24h;
    check_status $? "Application role applied." "There was an error during applying application role.";
}

function configure_kubernetes {
    local vault_install_path="$1";
    local kubernetes_namespace="$2";
    local vault_protocol="$3";
    local helm_custom_values_set_bool="$4";
    log_and_print "Configuring Kubernetes...";
    local files_to_apply=( app-namespace.yml vault-namespace.yml vault-default-policy.yml vault-service-account.yml app-service-account.yml )
    for file in "${files_to_apply[@]}" ; do
        if [ "$file" = "app-namespace.yml" ] && [ "$kubernetes_namespace" = "default" ]; then
            continue
        fi
        log_and_print "Applying $file...";
        kubectl apply -f "$vault_install_path/kubernetes/$file";
        check_status $? "$file: Success." "$file: Failure.";
    done
    log_and_print "Checking if Vault Agent Helm Chart is already installed...";
    helm list | grep vault;
    local command_result=( "${PIPESTATUS[@]}" );
    if [ "${command_result[0]}" != "0" ] ; then
        exit_with_error "There was an error during checking if Vault Agent Helm Chart is already installed. Exit status: ${command_result[0]}";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Vault Agent Helm Chart is already installed.";
    elif [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Installing Vault Agent Helm Chart...";
        if [ "$helm_custom_values_set_bool" = "true" ] ; then
          helm upgrade --install --wait -f /tmp/vault_helm_chart_values.yaml vault /tmp/v0.4.0.tar.gz --namespace vault
        else
          helm upgrade --install --wait vault /tmp/v0.4.0.tar.gz --namespace vault
        fi
        check_status $? "Vault Agent Helm Chart installed." "There was an error during installation of Vault Agent Helm Chart.";
    fi
}

function apply_epiphany_vault_policies {
    log_and_print "Applying Epiphany default Vault policies...";
    local vault_config_data_path="$1";
    vault policy write admin "$vault_config_data_path/policies/policy-admin.hcl";
    check_status $? "Admin policy applied." "There was an error during applying admin policy.";
    vault policy write provisioner "$vault_config_data_path/policies/policy-provisioner.hcl";
    check_status $? "Provisioner policy applied." "There was an error during applying provisioner policy.";
}

function enable_vault_userpass_authentication {
    log_and_print "Checking if userpass authentication is enabled...";
    vault auth list | grep userpass;
    local command_result=( "${PIPESTATUS[@]}" );
    if [ "${command_result[0]}" != "0" ] ; then
        exit_with_error "There was an error during listing authentication methods. Exit status: ${command_result[0]}";
    fi
    if [ "${command_result[1]}" = "0" ] ; then
        log_and_print "Userpass authentication is already enabled.";
    elif [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Turning on userpass authentication...";
        vault auth enable userpass;
        check_status $? "Userpass authentication enabled." "There was an error during enabling userpass authentication.";
    fi
}

function create_vault_user {
    local username="$1";
    local policy="$2";
    local token_path="$3";
    local token="$4";
    local vault_addr="$5";
    local override_existing_vault_users="$6";

    if [ ! -f "$token_path" ]; then
      touch "$token_path";
      chmod 0640 "$token_path";
    fi
    local users_path_response
    users_path_response=$(curl -o -I -L -s -w "%{http_code}" --header "X-Vault-Token: $token" --request LIST "$vault_addr/v1/auth/userpass/users");
    if (( users_path_response == 200 )) ; then
        curl --header "X-Vault-Token: $token" --request LIST "$vault_addr/v1/auth/userpass/users" | jq -e ".data.keys[] | select(.== \"$username\")";
        local command_result=$?;
    fi
    if [ "${override_existing_vault_users,,}" = "true" ] || (( users_path_response == 404 )) || (( command_result == 4 )); then
        log_and_print "Creating user: $username...";
        local password;
        password="$( < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c32 )";
        vault write "auth/userpass/users/$username" password="$password" policies="$policy";
        check_status $? "User: $username created." "There was an error during creation of user: $username.";
        echo "$username;$policy;$password;" >> "$token_path";
    elif [ "$command_result" = "0" ]; then
        log_and_print "$username already exists. Not adding or modyfing.";
        echo "$username;$policy;ALREADY_EXISTS;" >> "$token_path";
    else
        exit_with_error "There was a critical error during adding user: $username.";
    fi
}

function create_vault_users_from_file {
    local vault_install_path="$1";
    local token="$2";
    local vault_addr="$3";
    local override_existing_vault_users="$4";
    local users_csv_file_path="$vault_install_path/users.csv";
    local users_token_path="$vault_install_path/tokens-$(date +"%Y-%m-%d-%H%M%S").csv";
    local user_name
    local policy
    grep -v '#' "$users_csv_file_path" | while read -r line ; do
        user_name="$( echo "$line" | cut -d ';' -f 1 )";
        policy="$( echo "$line" | cut -d ';' -f 2 )";
        create_vault_user "$user_name" "$policy" "$users_token_path" "$token" "$vault_addr" "$override_existing_vault_users";
    done
}

function cleanup {
    rm -f "$HOME/.vault-token";
}

# --- Start ---

if [ "$#" -lt 6 ]; then
    print_help;
    exit_with_error "Mandatory argument is missing. Aborting.";
fi

while getopts ":a:c:p:v:h" opt; do
    case "$opt" in
        a) VAULT_IP=$OPTARG;;
        c) CONFIG_FILE=$OPTARG;;
        p) VAULT_PROTOCOL=$OPTARG;;
        v) HELM_CUSTOM_VALUES_SET_BOOL=$OPTARG;;
        \?) print_help; exit_with_error "Invalid parameter: -$OPTARG. Aborting.";;
        :) print_help; exit_with_error "Parameter -$OPTARG requires an argument. Aborting.";;
        h) print_help; exit 0;;
    esac
done
shift $((OPTIND-1))

test -f "$CONFIG_FILE" || exit_with_error "Config file not found. Aborting.";

# shellcheck source=/dev/null
source "$CONFIG_FILE";

INIT_FILE_PATH="$VAULT_INSTALL_PATH/init.txt"
VAULT_CONFIG_DATA_PATH="$VAULT_INSTALL_PATH/config"
PATH=$VAULT_INSTALL_PATH/bin:/usr/local/bin/:$PATH

export VAULT_ADDR="$VAULT_PROTOCOL://$VAULT_IP:8200"
export KUBECONFIG=/etc/kubernetes/admin.conf

if [ "${VAULT_TOKEN_CLEANUP,,}" = "true" ] ; then
    trap cleanup EXIT INT TERM;
fi

initialize_vault "$INIT_FILE_PATH";

if [ "${UNSEAL_VAULT,,}" = "true" ] ; then
    unseal_vault "$INIT_FILE_PATH";
fi

check_if_vault_is_unsealed;

log_and_print "Logging into Vault.";
LOGIN_TOKEN="$(grep "Initial Root Token:" "$INIT_FILE_PATH" | awk -F'[ ]' '{print $4}')";
vault login -no-print "$LOGIN_TOKEN";
check_status $? "Login successful." "There was an error while logging into Vault.";

if [ "${ENABLE_VAULT_AUDIT_LOGS,,}" = "true" ] ; then
    enable_vault_audit_logs;
fi

mount_secret_path "$SECRETS_ENGINE_PATH";

if [ "${KUBERNETES_INTEGRATION,,}" = "true" ]  || [ "${ENABLE_VAULT_KUBERNETES_AUTHENTICATION,,}" = "true" ] ; then
    enable_vault_kubernetes_authentication;
fi

apply_epiphany_vault_policies "$VAULT_CONFIG_DATA_PATH";
enable_vault_userpass_authentication;

if [ "${CREATE_VAULT_USERS,,}" = "true" ] ; then
    create_vault_users_from_file "$VAULT_INSTALL_PATH" "$LOGIN_TOKEN" "$VAULT_ADDR" "$OVERRIDE_EXISTING_VAULT_USERS";
fi

if [ "${KUBERNETES_CONFIGURATION,,}" = "true" ] ; then
    configure_kubernetes "$VAULT_INSTALL_PATH" "$KUBERNETES_NAMESPACE" "$VAULT_PROTOCOL" "$HELM_CUSTOM_VALUES_SET_BOOL";
fi

if [ "${KUBERNETES_INTEGRATION,,}" = "true" ] ; then
    integrate_with_kubernetes "$VAULT_CONFIG_DATA_PATH" "$KUBERNETES_NAMESPACE";
fi
