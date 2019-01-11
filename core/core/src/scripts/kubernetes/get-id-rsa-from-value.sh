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
# get-id-rsa-from-value.sh script get id rsa from variable and generate id_rsa key file
#

# Exit immediately if something goes wrong.
set -e;

# KEY_DIRECTORY - directory with id_rsa key
KEY_DIRECTORY=$1;
shift 1;
# ID_RSA_VARIABLE - string with id_rsa_variable content
ID_RSA_VARIABLE="$*";

echo "Creating $KEY_DIRECTORY directory"
mkdir -p "$KEY_DIRECTORY";
echo -e "$ID_RSA_VARIABLE" > "$KEY_DIRECTORY/id_rsa";
ls "$KEY_DIRECTORY/"
chmod og-rwx "$KEY_DIRECTORY/id_rsa";