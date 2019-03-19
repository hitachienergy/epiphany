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
MASTER_IP=$1
# KEY_DIRECTORY - directory with id_rsa key
KEY_DIRECTORY=$2;

MASTER_IP_CLEAN=$(echo $MASTER_IP | sed 's/\x1b\[[0-9;]*m//g')

# applies dashboard with sample user
ssh -l testadmin -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "kubectl apply -f /home/testadmin/linux/master/resources/kubernetes-dashboard.yml";
ssh -l testadmin -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "kubectl apply -f /home/testadmin/linux/master/resources/sample-role.yml";
ssh -l testadmin -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "kubectl apply -f /home/testadmin/linux/master/resources/role-binding.yml";
