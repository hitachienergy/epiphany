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

# This script updates /etc/hosts with newly provided ip address
# Run script:
# sudo ./1_update_hosts.sh "OLD_IP" "NEW_IP"

set -e

echo "==== Modifying /etc/hosts for new IP ===="

OLD_IP=$1
NEW_IP=$2

sed -i "s/$OLD_IP/$NEW_IP/g" "/etc/hosts"

echo "==== /etc/hosts modification completed ===="
