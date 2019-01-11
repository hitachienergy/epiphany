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
# get-init-token.sh script collects initial token and certificate hash from master and set this as VSTS parameter
#

# Exit immediately if something goes wrong.
set -e;

# MASTER_IP - IP of kubernetes master
MASTER_IP=$1;
# KEY_DIRECTORY - directory with id_rsa key
KEY_DIRECTORY=$2;
# MASTER_PASSWORD - password of user with sudo priviledge to run kubeadm
MASTER_PASSWORD=$3;
# USERNAME - user that will be used to login to servers
USERNAME=$4

# cleans IP parameter from end of line and other characters on VSTS
echo "Getting master IP. ";
MASTER_IP_CLEAN=$(echo $MASTER_IP | sed 's/\x1b\[[0-9;]*m//g')
echo "Master IP: $MASTER_IP_CLEAN";

# Gets kubernetes certificate hash
echo "Getting certificate hash.";
CERT_HASH=$(ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //');
echo "##vso[task.setvariable variable=certHash]$CERT_HASH";

# Gets kubernetes initial token
echo "Getting kubernetes cluster initial token."
TOKEN=$(ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "echo $MASTER_PASSWORD | sudo -S kubeadm token list | grep -i init");
TOKEN_TO_EXPORT=$(echo $TOKEN | grep -i init | awk '{print $1}')
echo "##vso[task.setvariable variable=token]$TOKEN_TO_EXPORT";