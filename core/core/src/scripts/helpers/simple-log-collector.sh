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

# USAGE: ./logs.sh /home/my_user/my_logs

OUTPUT_LOCATION=$1

log_locations=("/var/log/audit/audit.log" "/var/log/auth.log" "/var/log/firewalld" "/var/log/haproxy.log" "/var/log/kafka/server.log" "/var/log/messages" "/var/log/secure" "/var/log/syslog")

mkdir -p "$OUTPUT_LOCATION/$HOSTNAME"
printf "[CREATED]: Directory %s\n" "$OUTPUT_LOCATION/$HOSTNAME"

for ix in ${!log_locations[*]}
do
    
    if [ -f ${log_locations[$ix]} ]
    then
        file_name="$(basename ${log_locations[$ix]})"
        output_file_path="$OUTPUT_LOCATION/$HOSTNAME/$file_name"
        cp "${log_locations[$ix]}" "$output_file_path"
        printf "[COPIED]: %s to %s/%s \n" "${log_locations[$ix]}" "$output_file_path"
    else
        printf "[SKIPPED]: Not exists: %s\n" "${log_locations[$ix]}"
    fi
done
echo

if [ -x "$(command -v docker)" ]; then
  containers=$(sudo docker ps -a | awk '{if(NR>1) print $NF}')
  for container in $containers
  do
    docker_logs_path="$OUTPUT_LOCATION/$HOSTNAME/$container"
    sudo docker logs $container &> $docker_logs_path
    printf "[CREATED]: Docker logs %s \n" "$docker_logs_path"
  done
else
  echo "[SKIPPED]: No docker found."
fi
