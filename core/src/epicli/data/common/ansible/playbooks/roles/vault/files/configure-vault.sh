#!/bin/bash

VAULT_INSTALL_PATH=$1
INIT_FILE_PATH=$VAULT_INSTALL_PATH/test.txt
VAULT_IP=$2
AUTO_UNSEAL=$3

export PATH=$VAULT_INSTALL_PATH/bin:$PATH

if [ "$AUTO_UNSEAL" = true ] ; then
  grep -m 3 Unseal $INIT_FILE_PATH | awk '{print $4}' | while read -r line ; do
    vault operator unseal -address="http://$VAULT_IP:8200" "$line";
    if [ $? != 1 ] ; then
        echo "Done";
    fi
  done
fi

LOGIN_TOKEN=$(grep "Initial Root Token:" $INIT_FILE_PATH | awk -F'[ ]' '{print $5}');

vault login -address="http://$VAULT_IP:8200" $LOGIN_TOKEN;

vault secrets list -address="http://$VAULT_IP:8200" | grep "secret/";

if [ $? = 1 ] ; then
   vault secrets enable -path=secret -address="http://$VAULT_IP:8200" kv-v2;
fi

rm -f $HOME/.vault-token
