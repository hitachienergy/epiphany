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

# IMPORTANT!
# Requires sudo permissions
# Can be executed ONLY after changing IPs - since it will regenerate certificates using current IP address. 

echo "[INFO] This script should be run after changing IP address on the machine"
echo "==== Regenarating Kubernetes certificates with new IP ===="

cd /etc/kubernetes/pki

rm apiserver.crt apiserver.key
kubeadm init phase certs apiserver

rm etcd/peer.crt etcd/peer.key
kubeadm init phase certs etcd-peer

systemctl restart kubelet
systemctl restart docker

sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config

echo "==== Regenarating Kubernetes certificates completed ===="