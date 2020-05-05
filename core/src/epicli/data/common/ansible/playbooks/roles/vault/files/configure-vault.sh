#!/bin/bash
# Add proper error handling

VAULT_INSTALL_PATH=$1
INIT_FILE_PATH=$VAULT_INSTALL_PATH/test.txt
VAULT_IP=$2
AUTO_UNSEAL=$3

export PATH=$VAULT_INSTALL_PATH/bin:$PATH

if [ "$AUTO_UNSEAL" = true ] ; then
  grep -m 3 Unseal $INIT_FILE_PATH | awk '{print $4}' | while read -r line ; do
    vault operator unseal -address="http://$VAULT_IP:8200" "$line";
    # TODO: Add proper error handling
  done
fi

vault secrets list -address="http://$VAULT_IP:8200" | grep "secret/"

# TODO: Add login to vault

if [ $? = 1 ] ; then
   vault secrets enable -path=secret -address="http://$VAULT_IP:8200" kv-v2
fi
