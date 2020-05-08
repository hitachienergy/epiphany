#!/bin/bash
# TODO: Revoke root token
# TODO: Policy for non-root access
# TODO: Rewrite to functions
# TODO: Enable kubernetes authentication

#set -o errexit -o pipefail;

HELP_MESSAGE="Usage: configure-vault.sh
-p path to vault installation folder
-a vault ip address
-u vault script unseal - true/false
-k kubernetes integration - true/false
-l log directory
-s secret mount path"
LOG_DIR="/var/log/vault";

function print_help { echo "$HELP_MESSAGE"; }

while getopts ":p:a:Aus:kl:h?" opt; do
    case "$opt" in
        p) VAULT_INSTALL_PATH=$OPTARG;;
        a) VAULT_IP=$OPTARG;;
        A) ENABLE_AUDITING=$OPTARG;;
        u) AUTO_UNSEAL=$OPTARG;;
        s) SECRET_PATH=$OPTARG;;
        k) KUBERNETES_INTEGRATION=$OPTARG;;
        l) LOG_DIR=$OPTARG;;
        ? | h | *) print_help; exit 2;;
    esac
done

if [ $OPTIND -eq 1 ]; then
    echo "No options passed";
    print_help;
    exit 2;
fi

INIT_FILE_PATH="$VAULT_INSTALL_PATH/init.txt"
export VAULT_ADDR="http://$VAULT_IP:8200"
PATH=$VAULT_INSTALL_PATH/bin:$PATH

if [ "$AUTO_UNSEAL" = "true" ] ; then
  echo "Unsealing vault.";
  grep -m 3 Unseal "$INIT_FILE_PATH" | awk '{print $4}' | while read -r line ; do
    vault operator unseal "$line";
    if [ $? != 1 ] ; then
        echo "Done";
    fi
  done
fi

echo "Loging to vault."
LOGIN_TOKEN="$(grep "Initial Root Token:" "$INIT_FILE_PATH" | awk -F'[ ]' '{print $4}')";
vault login -no-print "$LOGIN_TOKEN";
LOGIN_TOKEN="";

if [ "$ENABLE_AUDITING" = "true" ] ; then
    echo "Enabling auditing.";
    vault audit list | grep "file";

    if [ "$?" = "1" ] ; then
        vault audit enable file file_path="$LOG_DIR/audit.log";
    fi
fi

vault secrets list | grep "$SECRET_PATH/";

if [ "$?" = "1" ] ; then
   vault secrets enable -path="$SECRET_PATH" kv-v2;
fi

#if [ "$KUBERNETES_INTEGRATION" = "true" ] ; then
#
#fi

rm -f "$HOME/.vault-token"
