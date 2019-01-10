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

#run-sonobuoy-test.sh will launch sonobuoy (https://github.com/heptio/sonobuoy) tests on existing cluser and will wait for test suite to finish. 
#When tests will finish their work, result will be retrieved and copied to location defined in this script. 

#prerequisites:
#1. Installed kubectl tool
#2. Installed golang in min version 1.9.1. 
#3. KUBECONFIG environment variable set to location of Kubernetes config file 
#4. Sonobuoy package installed (install-test-prerequisites.sh)
#5. GOPATH environment set to Go packages location 

#Running this script take a long time because of number of test that have to be executed. If script execution will be interrupted, make sure sonobuoy tool will be stopped as well
#by calling "sonobuoy delete", it is required because only one test suite can be executed at cluster at time.  

sonobuoy run
TIME_TO_WAIT="1m"
TEST_RESULTS_LOCATION="$HOME/sonobuoy-results/"

#until loop will wait for plugins to finish their work. 
echo "It will take about 70 minutes to complete all tests."
sleep 1m ; 
COMPLETED_NUMBER=$(sonobuoy status | grep -c "complete")
COUNTER=1
until [ $COMPLETED_NUMBER -ge "2" ]; do 
printf "Already waiting: %s minutes for results \n" "$COUNTER"
sleep $TIME_TO_WAIT ; 
COMPLETED_NUMBER=$(sonobuoy status | grep -c "complete")
let COUNTER+=1
done

mkdir $TEST_RESULTS_LOCATION
sonobuoy retrieve $TEST_RESULTS_LOCATION

cd $TEST_RESULTS_LOCATION
RESULT_FILE_LOCATION=$(ls .)

sonobuoy e2e $RESULT_FILE_LOCATION --show=passed
sonobuoy e2e $RESULT_FILE_LOCATION --show=failed

tar xzf $TEST_RESULTS_LOCATION*.tar.gz -C $TEST_RESULTS_LOCATION
find $TEST_RESULTS_LOCATION -type f -iname "e2e.txt" -exec cat {} \;
sonobuoy delete

