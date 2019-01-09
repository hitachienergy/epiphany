#!/bin/bash
#
# Copyright 2019 ABB. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# init-kubernetes-nodes.sh script that join node to kubernetes master
#

# Exit immediately if something goes wrong.
set -e;

# NODE_IP - IP of node that you want to join kubernetes master
NODE_IP=$1;
# CERT_HASH - hash of certificate from kubernetes master
CERT_HASH=$2;
# TOKEN - token to join kubernetes master
TOKEN=$3;
# KEY_DIRECTORY - directory with id_rsa key
KEY_DIRECTORY=$4;
# ADMIN_PASSWORD - password to execute kubeadm join with sudo
ADMIN_PASSWORD=$5;
# USERNAME - user that will be used to execute ssh command
USERNAME=$6
# MASTER_ADDRESS -kubernetes master address
MASTER_ADDRESS=$7

echo "IP: $NODE_IP";
echo "Key Directory: $KEY_DIRECTORY";

# cleans IP parameter from end of line and other characters on VSTS
NODE_IP_CLEAN=$(echo $NODE_IP | sed 's/\x1b\[[0-9;]*m//g')
MASTER_ADDRESS_CLEAN=$(echo $MASTER_ADDRESS | sed 's/\x1b\[[0-9;]*m//g')

# set no_proxy environment variable for node to skip proxy when trying to call master node
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$NODE_IP_CLEAN" "echo 'export no_proxy=\"127.0.0.1, localhost, $MASTER_IP_CLEAN, $MASTER_IP_CLEAN:6443, $NODE_IP_CLEAN\"' >> $HOME/.bashrc";

echo "Joining kubernetes master.";
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$NODE_IP_CLEAN" "echo $ADMIN_PASSWORD | sudo -S kubeadm join $MASTER_ADDRESS_CLEAN:6443 --token $TOKEN --discovery-token-ca-cert-hash sha256:$CERT_HASH";