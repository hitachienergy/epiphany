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

#Run this script on every Slave which you've got

echo "==== Modifying /var/lib/postgresql/.pgpass for new IP ===="

#OLD_IP_MASTER - Address which will be modified
#NEW_IP_MASTER - Updated value 

OLD_IP_MASTER=$1
NEW_IP_MASTER=$2

sed -i "s/$OLD_IP_MASTER/$NEW_IP_MASTER/g" "/var/lib/postgresql/.pgpass"

echo "==== /var/lib/postgresql/.pgpass modification completed ===="