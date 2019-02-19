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
# MASTER_PASSWORD - password of user with sudo priviledge to run kubeadm
MASTER_PASSWORD=$3;
# USERNAME - user that will be used to login to servers
USERNAME=$4

MASTER_IP_CLEAN=$(echo $MASTER_IP | sed 's/\x1b\[[0-9;]*m//g')
MASTER_API_ADDRESS="https://$MASTER_IP_CLEAN:6443"

# initializes kubernetes with kubeadm
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "echo $MASTER_PASSWORD | sudo -S kubeadm init --pod-network-cidr 10.244.0.0/16 --apiserver-cert-extra-sans=$MASTER_IP_CLEAN";

# creating configuration for user $USERNAME to be able to connect to master with kubectl
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "mkdir -p /home/$USERNAME/.kube";
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "echo $MASTER_PASSWORD | sudo -S cp -i /etc/kubernetes/admin.conf /home/$USERNAME/.kube/config";
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "echo $MASTER_PASSWORD | sudo -S chown $USERNAME:$USERNAME /home/$USERNAME/.kube/config";

# set no_proxy setting to skip proxy when accessing API Server 
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "echo 'export no_proxy=\"127.0.0.1, localhost, $MASTER_IP_CLEAN, $MASTER_IP_CLEAN:6443\"' >> $HOME/.bashrc";

# modify Kubernetes config files to use dns name
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "sed -i 's|server: https://.*|server: $MASTER_API_ADDRESS|g' /home/$USERNAME/.kube/config";
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "echo $MASTER_PASSWORD | sudo -S sed -i 's|server: https://.*|server: $MASTER_API_ADDRESS|g' /etc/kubernetes/admin.conf";
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "echo $MASTER_PASSWORD | sudo -S sed -i 's|server: https://.*|server: $MASTER_API_ADDRESS|g' /etc/kubernetes/kubelet.conf";
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "echo $MASTER_PASSWORD | sudo -S sed -i 's|server: https://.*|server: $MASTER_API_ADDRESS|g' /etc/kubernetes/controller-manager.conf";
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "echo $MASTER_PASSWORD | sudo -S sed -i 's|server: https://.*|server: $MASTER_API_ADDRESS|g' /etc/kubernetes/scheduler.conf";

systemctl daemon-reload && systemctl restart kubelet

# applies kube-flannel network overlay to kubernetes cluster
ssh -l $USERNAME -i "$KEY_DIRECTORY/id_rsa" -oStrictHostKeyChecking=no "$MASTER_IP_CLEAN" "kubectl apply -f /home/$USERNAME/linux/master/resources/kube-flannel.yml";

