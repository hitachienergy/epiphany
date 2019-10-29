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

OLD_IP=$1 
NEW_IP=$2

echo "==== Modifying All config maps for Kubernetes ===="

namespaces=$(kubectl get ns | \
  awk '{print $1}' | \
  cut -d '/' -f 2)

for ns in $namespaces; do

    # find all the config map names
    configmaps=$(kubectl -n $ns get cm -o name | \
    awk '{print $1}' | \
    cut -d '/' -f 2)

    # fetch all for filename reference
    dir=$(mktemp -d)
    for cf in $configmaps; do
    kubectl -n $ns get cm $cf -o yaml > $dir/$cf.yaml
    done

    # have grep help you find the files to edit, and where
    grep -Hn $dir/* -e $OLD_IP
    find $dir/ -type f -name "*.yaml" -print0 | xargs -0 sed -i "s/$OLD_IP/$NEW_IP/g"

    for filename in $dir/*.yaml; do
        kubectl apply -f $filename
    done

done

echo "==== Config map modification completed ===="