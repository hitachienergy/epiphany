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

# Summary:
# This script builds out the required terraform, scripts, json, yaml, etc. files and executes
# them. The goal is to create the required Azure infrastructure using Terraform, collect
# cluster information using 'az' where needed and finally build out the required Ansible
# inventory and other files required to bootstrap the environment.
#
# The bootstrap data files are used regardless of platform. If on-premise the customer
# provides IPs, gateways, firewall data, MAC Addresses (if needed) and more. This data is then
# used to create the bootstrap data files and then Ansible loads all of the required files,
# executes any scripts required and preps for the next layer.

# NOTE: Other scripts may call this script so do not change parameters unless you know the impact!

# MUST HAVE SUDO RIGHTS FOR YOUR ACCOUNT! DON'T USE 'sudo gen_helper.sh' but have sudo rights.

# Can use 'basename' to extract name from parameter 1 and assign it to parameter 2. This can be done
# in a higher level helper script if desired.

# run_build.sh just makes it easier to call gen_templates_azure.sh for Azure

# Exit immediately if something goes wrong.
set -e

export REPO_ROOT=$(git rev-parse --show-toplevel)/core

COMMON_SCRIPTS_BASE=core/src/scripts/common
COMMON_TEMPLATES_BASE=core/src/templates/common

SCRIPTS_BASE=core/src/scripts/azure
TEMPLATES_BASE=core/src/templates/azure

DATA_DIR=$1
OUTPUT_DIR=$2
EPIPHANY_DATA_DIR=$3
DATA=$4

# Set in var name in the event we want to override or allow for passing in a different name.
if [[ -z $DATA ]]; then
    DATA=data.yaml
fi

source $REPO_ROOT/$COMMON_SCRIPTS_BASE/base_colors.sh

if [[ -z $DATA_DIR ]]; then
    echo_red '====> ERROR: MUST specify a valid DATA directory! <===='
    exit 1
fi

if [[ -z $OUTPUT_DIR ]]; then
    echo_red '====> ERROR: MUST specify a valid OUTPUT directory! <===='
    exit 1
fi

# This extracts the last portion of the path or the word if no path. This is the final Terraform file name.
OUTPUT_TF_FILE=${DATA_DIR##*/}

if [[ -z $OUTPUT_TF_FILE ]]; then
    echo_red '====> ERROR: MUST specify the Terraform output file name! <===='
    exit 1
fi

# Make sure the output directory exists
mkdir -p $OUTPUT_DIR

export TF_IN_AUTOMATION=1

$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/version.sh.j2 -o $OUTPUT_DIR/version.sh
chmod +x $OUTPUT_DIR/version.sh
source $OUTPUT_DIR/version.sh

echo
echo_yellow '====> Creating gen_sp.sh...'

# If not enabled then gen_sp.sh will only be a stub
$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/gen_sp.sh.j2 -o $OUTPUT_DIR/gen_sp.sh
chmod +x $OUTPUT_DIR/gen_sp.sh

# Generate the script to delete the resource group
$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/del_rg.sh.j2 -o $OUTPUT_DIR/del_rg.sh
chmod +x $OUTPUT_DIR/del_rg.sh

# NOTE:
# IF you want to delete the resource group and service principal then do so in the following order:
# 1. ./del_sp.sh
# 2. ./del_rg.sh
# Verify the resource group has been deleted or is still being purged via the Azure Portal. You can check for the existence of
# the resource group via Azure CLI but we don't do that.

echo_yellow '====> Check for service principal being enabled...'

az logout &2>/dev/null || echo "No session to remove.";

if [[ -f $OUTPUT_DIR/az_ad_sp.json ]]; then
	
	echo "File az_ad_sp.json exists."
	cat $OUTPUT_DIR/az_ad_sp.json | grep 'appId'
    
	if [[ $? -ne 0 ]]; then
        
		echo "File corrupted. Removing. Please login manually."
		rm -f $OUTPUT_DIR/az_ad_sp.json
		
    else
	
		echo "Logging with Service Principal from from az_ad_sp.json."
		SP_CLIENT_ID=$(grep -i appId $OUTPUT_DIR/az_ad_sp.json | awk '{print $2}' | tr -d "\"" | tr -d ",")
		SP_CLIENT_SECRET=$(grep -i password $OUTPUT_DIR/az_ad_sp.json | awk '{print $2}' | tr -d "\"" | tr -d ",")
		SP_TENANT_ID=$(grep -i tenant $OUTPUT_DIR/az_ad_sp.json | awk '{print $2}' | tr -d "\"" | tr -d ",")
	
		az login --service-principal -u $SP_CLIENT_ID -p $SP_CLIENT_SECRET --tenant $SP_TENANT_ID
		
	fi
fi

# Make sure to force a login with enough rights to create service principals. Could create a process later that
# creates certs to use for all 'az' commands...
# testing...
if [[ ! -f $OUTPUT_DIR/az_ad_sp.json ]]; then
    if [[ -f $OUTPUT_DIR/../epiphan_azure_cert.pem ]]; then
        #WIP az login --service-principal ...
        echo 'wip'
    else
        # For security - login each time unless a service principal is used
        az login
    fi
fi

echo "Running gen_sp.sh script."
$OUTPUT_DIR/gen_sp.sh $DATA_DIR $OUTPUT_DIR $OUTPUT_TF_FILE $DATA
echo "Logging to Azure."
$OUTPUT_DIR/login.sh $DATA_DIR $OUTPUT_DIR $OUTPUT_TF_FILE $DATA

source $OUTPUT_DIR/env.sh $DATA_DIR

# NOTE: Check for terraform backends first! If using backend then create resource group, storage account and container first.
# Then get key1 for access_key, generate config.tfvars, backend.tf and run 'terraform init -backend-conf=config.tfvars -backend-config="access_key=<value>"'

# Create resources now
echo_yellow '====> Creating base.tf...'

$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/base.tf.j2 -o $OUTPUT_DIR/base.tf

if [[ ! -f $OUTPUT_DIR/terraform.init ]]; then
    # This means Terraform is starting over so we need to check ./terraform directory for terraform.tfstate and remove it
    if [[ -f $OUTPUT_DIR/.terraform/terraform.tfstate ]]; then
        rm -f $OUTPUT_DIR/.terraform/terraform.tfstate
    fi

    (cd $OUTPUT_DIR && terraform init $OUTPUT_DIR)

    # NOTE:
    # If you receive an error from Terraform like the following:
    # Error: Error running plan: 1 error(s) occurred:
    # * provider.azurerm: Unable to list provider registration status
    #
    # This is most likely due to NOT being logged into Azure. Call `az login` and it will give you a device key. Copy that and load 'https://microsoft.com/devicelogin' and then paste it into the prompt and apply. It will then log you in and give your CLI a token
    # to use for a short time.

    # Create the resources
    (cd $OUTPUT_DIR && terraform apply -auto-approve $OUTPUT_DIR)

    echo "# Terraform init has been completed - ONLY remove this file if you want it to run again!" > $OUTPUT_DIR/terraform.init
fi

echo_yellow '====> Creating backend.tf...'

$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/backend.sh.j2 -o $OUTPUT_DIR/backend.sh
chmod +x $OUTPUT_DIR/backend.sh
$OUTPUT_DIR/backend.sh $DATA_DIR $OUTPUT_DIR $OUTPUT_TF_FILE $DATA

echo_yellow "====> Calling ==> ${REPO_ROOT}/${SCRIPTS_BASE}/gen_templates_azure.sh ${DATA_DIR} ${OUTPUT_DIR} ${OUTPUT_TF_FILE} ${DATA} <=="

$REPO_ROOT/$SCRIPTS_BASE/gen_templates_azure.sh $DATA_DIR $OUTPUT_DIR $OUTPUT_TF_FILE $DATA

source $OUTPUT_DIR/env.sh $DATA_DIR

# Create the resources
echo_yellow "====> Applying plan to resources..."

# Terraform requires you to run in the directory of the *.tf files.

(cd $OUTPUT_DIR && terraform apply -auto-approve $OUTPUT_DIR)

# Extract the output variables and build the terraform.json file that is used to build Ansible inventory data
echo_yellow '====> Gathering Terraform IP addresses...'

(cd $OUTPUT_DIR && terraform output -json > $OUTPUT_DIR/terraform.json)



# Gather IP and host names from Azure
echo_yellow '====> Gathering Azure IP addresses...'

$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/az_get_ips.sh.j2 -o $OUTPUT_DIR/az_get_ips.sh
chmod +x $OUTPUT_DIR/az_get_ips.sh
$OUTPUT_DIR/az_get_ips.sh $OUTPUT_DIR

# This will generate the data file that will be common to all platforms, not just terraform
echo_yellow '====> Generating manifest.yaml...'
#cat $DATA_DIR/$DATA > $OUTPUT_DIR/data_with_ips.yaml
$REPO_ROOT/bin/template_engine -d $OUTPUT_DIR/az_vm_ips.json -y >> $OUTPUT_DIR/azure_hosts.yaml
$REPO_ROOT/bin/template_engine -d $OUTPUT_DIR/terraform.json -y >> $OUTPUT_DIR/azure_storage_keys.yaml

chmod +x $REPO_ROOT/$SCRIPTS_BASE/fill_in_manifest.py
$REPO_ROOT/$SCRIPTS_BASE/fill_in_manifest.py -d $DATA_DIR/$DATA -a $OUTPUT_DIR/azure_hosts.yaml -k $OUTPUT_DIR/azure_storage_keys.yaml -t $REPO_ROOT/$COMMON_TEMPLATES_BASE/manifest.yaml.j2 -o $EPIPHANY_DATA_DIR/data/manifest.yaml

echo_yellow '====> Generating infrastructure release...'


$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/release.sh.j2 -o $OUTPUT_DIR/release.sh
chmod +x $OUTPUT_DIR/release.sh
$OUTPUT_DIR/release.sh $DATA_DIR $OUTPUT_DIR $OUTPUT_TF_FILE $DATA

# Make sure you're logged out
az logout &2>/dev/null
