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
# prepare-system-kubernetes-redhat.sh script that initialize operating system configuration to be able to run kubernetes
#

# Exit immediately if something goes wrong.
set -e

# turns off se linux enforce for session
setenforce 0;
# turns off se linux enforce pernamently
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux;

# turns off swap enabled by default on red hat on azure
swapoff -a

# installs and enable docker daemon
yum install -y docker;
systemctl enable docker;
groupadd docker && usermod -aG docker $USER
systemctl restart docker

# add kubernetes repository
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

# installs and enable kubelet daemon
yum install -y kubelet kubeadm kubectl;
systemctl enable kubelet && systemctl start kubelet;

# disable firewalld to avoid problems with connection
# TODO: create firewalld setup to work with kubernetes
systemctl stop firewalld;
systemctl disable firewalld;