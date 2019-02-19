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

#install-test-prerequisites.sh will install golang and sonobuoy components. 
#Script require internet connection in order to download golang binaries and sonobuoy plugin. 
#PATH environment variable will be updated with go binaries folder (GOROOT) and go packages folder (GOPATH).  

sudo yum install -y git

mkdir /tmp/k8s-test
cd /tmp/k8s-test

curl -O https://storage.googleapis.com/golang/go1.9.1.linux-amd64.tar.gz
tar -xvf go1.9.1.linux-amd64.tar.gz
sudo mv go /usr/local

export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export PATH=$GOROOT/bin:$GOPATH/bin:$PATH 

#install go component - sonobuoy, it will create $HOME/go path if the path did not exist. 
go get -u -v github.com/heptio/sonobuoy

echo GOROOT=/usr/local/go >> $HOME/.profile
echo GOPATH=$HOME/go >> $HOME/.profile
echo PATH=$GOROOT/bin:$GOPATH/bin:$PATH >> $HOME/.profile

#Print version of installed components. 
go version
SONOBUOY_VERSION=$(sonobuoy version)
echo "sonobuoy version: $SONOBUOY_VERSION"


