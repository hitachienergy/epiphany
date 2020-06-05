#!/bin/bash
# Description: This script configures Hashicorp Vault to be used with Epiphany
# You can find more information in Epiphany documentation in HOWTO.md
# TODO: Revoke root token
# TODO: Add flag to override existing users
# TODO: Add flag to enable/disable token cleanup
# TODO: Add catching exit 2 in check_vault_error
# TODO: Configuration of unsealing after server restart with script

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
    if [ "${command_result[0]}" != "0"] ; then
        exit_with_error "There was an error during listing auditing. Exit status: ${command_result[0]}";
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
    if [ "${command_result[0]}" != "0" ] ; then
        exit_with_error "There was an error during listing secret engines. Exit status: ${command_result[0]}";
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
    if [ "${command_result[0]}" != "0" ] ; then
        exit_with_error "There was an error during listing authentication methods. Exit status: ${command_result[0]}";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Turning on Kubernetes authentication...";
        vault auth enable kubernetes;
        check_vault_error "$?" "Kubernetes authentication enabled." "There was an error during enabling Kubernetes authentication.";
    fi
}

function integrate_with_kubernetes {
    local vault_config_data_path="$1";

    log_and_print "Turning on Kubernetes integration...";
    local token_reviewer_jwt="$(kubectl --kubeconfig=/etc/kubernetes/admin.conf get secret vault-auth -o go-template='{{ .data.token }}' | base64 --decode)";
    local kube_ca_cert=$(kubectl --kubeconfig=/etc/kubernetes/admin.conf config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}' | base64 --decode);
    local kube_host=$(kubectl --kubeconfig=/etc/kubernetes/admin.conf config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.server}');
    vault write auth/kubernetes/config token_reviewer_jwt="$token_reviewer_jwt" kubernetes_host="$kube_host" kubernetes_ca_cert="$kube_ca_cert";
    check_vault_error "$?" "Kubernetes parameters written to auth/kubernetes/config." "There was an error during writing kubernetes parameters to auth/kubernetes/config.";
    vault policy write devweb-app $vault_config_data_path/policy-application.hcl;
    check_vault_error "$?" "Application policy applied." "There was an error during applying application policy.";
    vault write auth/kubernetes/role/devweb-app bound_service_account_names=internal-app bound_service_account_namespaces=default policies=devweb-app ttl=24h;
    check_vault_error "$?" "Admin policy applied." "There was an error during applying admin policy.";
}

function configure_kubernetes {
    local vault_install_path="$1";

    log_and_print "Configuring kubernetes...";
    log_and_print "Applying vault-endpoint-configuration.yml...";
    kubectl apply -f "$vault_install_path/kubernetes/vault-endpoint-configuration.yml";
    log_and_print "Applying vault-service-account.yml...";
    kubectl apply -f "$vault_install_path/kubernetes/vault-service-account.yml";
    log_and_print "Applying app-service-account.yml...";
    kubectl apply -f "$vault_install_path/kubernetes/app-service-account.yml";
    log_and_print "Checking if Vault Agent Helm Chart is already installed...";
    helm list | grep vault;
    local command_result=( ${PIPESTATUS[@]} );
    if [ "${command_result[0]}" != "0" ] ; then
        exit_with_error "There was an error during checking if Vault Agent Helm Chart is already installed. Exit status: ${command_result[0]}";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Installing Vault Agent Helm Chart...";
        helm install vault --set "injector.externalVaultAddr=http://external-vault:8200" https://github.com/hashicorp/vault-helm/archive/v0.4.0.tar.gz
        check_vault_error "$?" "Vault Agent Helm Chart installed." "There was an error during installation of Vault Agent Helm Chart.";
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
    if [ "${command_result[0]}" != "0" ] ; then
        exit_with_error "There was an error during listing authentication methods. Exit status: ${command_result[0]}";
    fi
    if [ "${command_result[1]}" = "1" ] ; then
        log_and_print "Turning on userpass authentication...";
        vault auth enable userpass;
        check_vault_error "$?" "Userpass authentication enabled." "There was an error during enabling userpass authentication.";
    fi
}

function create_vault_user {
    local username="$1";
    local policy="$2";
    local token_path="$3";
    local token="$4";
    local vault_addr="$5";

    if [ -f "$token_path" ]; then
      touch $token_path;
      chmod 0640 $token_path;
    fi
    local users_path_response=$(curl -o -I -L -s -w "%{http_code}" --header "X-Vault-Token: $token" --request LIST "$VAULT_ADDR/v1/auth/userpass/users");
    curl --header "X-Vault-Token: $token" --request LIST "$vault_addr/v1/auth/userpass/users" | jq -e ".data.keys[] | select(.== \"$username\")";
    local local command_result="$?";
    echo "Command result: $command_result";
    if [ $users_path_response -eq 404 ] || [ "$command_result" = "4" ]; then
        log_and_print "Creating user: $username...";
        local password="$( < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c32 )";
        vault write auth/userpass/users/$username password=$password policies=$policy;
        check_vault_error "$?" "User: $username created." "There was an error during creation of user: $username.";
        echo "$username;$policy;$password;" >> $token_path;
    elif [ "$command_result" = "0" ]; then
        log_and_print "$username already exists. Not adding or modyfing.";
        echo "$username;$policy;ALREADY_EXISTS;" >> $token_path;
    else
        exit_with_error "There was an critical error during adding user $username.";
    fi
}

# TODO: Add flag to override existing users
function create_vault_users_from_file {
    local vault_install_path="$1";
    local users_file_csv_path="$vault_install_path/users.csv";
    local users_token_path="$vault_install_path/tokens-`date +"%Y-%m-%d-%H%M%S"`.csv";
    local token="$2";
    local vault_addr="$3";

    cat $users_file_csv_path | while read -r line ; do
        local username="$( echo $line | cut -d ';' -f 1 )";
        local policy="$( echo $line | cut -d ';' -f 2 )";
        create_vault_user "$username" "$policy" "$users_token_path" "$token" "$vault_addr";
    done
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
export KUBECONFIG=/etc/kubernetes/admin.conf
PATH=$VAULT_INSTALL_PATH/bin:/usr/local/bin/:$PATH

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
#LOGIN_TOKEN="";

if [ "${ENABLE_AUDITING,,}" = "true" ] ; then
    enable_vault_audit_logs;
fi

mount_secret_path "$SECRET_PATH";

if [ "${KUBERNETES_INTEGRATION,,}" = "true" ]  || [ "${ENABLE_VAULT_KUBERNETES_AUTHENTICATION,,}" = "true" ] ; then
    enable_vault_kubernetes_authentication;
fi

apply_epiphany_vault_policies "$VAULT_CONFIG_DATA_PATH";
enable_vault_userpass_authentication;
create_vault_users_from_file "$VAULT_INSTALL_PATH" "$LOGIN_TOKEN" "$VAULT_ADDR";

if [ "${KUBERNETES_INTEGRATION,,}" = "true" ] ; then
    integrate_with_kubernetes "$VAULT_CONFIG_DATA_PATH";
fi

if [ "${KUBERNETES_CONFIGURATION,,}" = "true" ] ; then
    configure_kubernetes "$VAULT_INSTALL_PATH";
fi
