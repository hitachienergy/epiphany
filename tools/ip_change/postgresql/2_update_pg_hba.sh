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

#Run this script on Master as many times as many Slaves you've got
set -e

#OLD_IP_SLAVE - Address which will be modified
#NEW_IP_SLAVE - Updated value

OLD_IP_SLAVE=$1
NEW_IP_SLAVE=$2

echo "==== Modifying /etc/postgresql/10/main/pg_hba.conf for new IP ===="

sed -i "s/$OLD_IP_SLAVE/$NEW_IP_SLAVE/g" "/etc/postgresql/10/main/pg_hba.conf"

echo "==== /etc/postgresql/10/main/pg_hba.conf modification completed ===="
