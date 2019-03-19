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
# prepare-system-kubernetes-ubuntu.sh script that initialize operating system configuration to be able to run kubernetes
#

# Exit immediately if something goes wrong.
set -e

# turns off all swaps
# swap off - can be needed on prem, disabled by default on ubuntu on azure
# swapoff -a

# installs docker and dependencies needed by kubernetes
apt-get update && apt-get upgrade -y
apt-get install -y docker.io apt-transport-https curl mc

# adds key and repository with kubernetes
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF

# installs kubernetes
apt-get update
apt-get install -y kubelet kubeadm kubectl
