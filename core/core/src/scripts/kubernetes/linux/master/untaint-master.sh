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
# init-kubernetes-nodes.sh script that initialize kubernetes master
#

# Exit immediately if something goes wrong.
set -e;

# MASTER_IP - IP of kubernetes master
MASTER_IP=$1;
# KEY_DIRECTORY - directory with id_rsa key
KEY_DIRECTORY=$2;

# cleans IP parameter from end of line and other characters on VSTS
echo "Getting master IP. ";
MASTER_IP_CLEAN=$(echo $MASTER_IP | sed 's/\x1b\[[0-9;]*m//g')
echo "Master IP: $MASTER_IP_CLEAN";

REMOTE_HOSTNAME=$(ssh -l testadmin -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "cat /proc/sys/kernel/hostname");
echo "Remote hostname: $REMOTE_HOSTNAME";
KUBECTL_OUTPUT=$(ssh -l testadmin -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "kubectl get nodes | grep -i $REMOTE_HOSTNAME");
NODE_TO_UNTAINT=$(echo $KUBECTL_OUTPUT | awk '{print $1}');
echo "Untaint node: $NODE_TO_UNTAINT";
ssh -l testadmin -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "kubectl taint node $NODE_TO_UNTAINT node-role.kubernetes.io/master:NoSchedule-";
