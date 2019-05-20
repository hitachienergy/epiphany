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

# NOTE: Other scripts may call this script so do not change parameters unless you know the impact!

# version.sh Sets the environment variables - ONLY 'source' this script.

# Exit immediately if something goes wrong.
set -e

unset EPIPHANY_VERSION
unset EPIPHANY_VERSION_NAME

export EPIPHANY_VERSION="0.2.2"
export EPIPHANY_VERSION_NAME="Epiphany"