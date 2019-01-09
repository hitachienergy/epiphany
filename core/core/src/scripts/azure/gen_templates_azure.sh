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

# gen_terraform_template.sh will generate the correct Terraform .tf files based on the following:
# Main templates:
# 1. main.tf.j2
# 2. outputs.tf.j2
# 3. variables.tf.j2  (Note: This file may be empty)

# Data file:
# 1. data.yaml (Note: This file is in a directory that is passed to this script)

# Exit immediately if something goes wrong.
set -e

TEMPLATES_BASE=core/src/templates/azure

# Get the root of the Epiphany repo
export REPO_ROOT=$(git rev-parse --show-toplevel)/core

COMMON_SCRIPTS_BASE=core/src/scripts/common
COMMON_TEMPLATES_BASE=core/src/templates/common

DATA_DIR=$1
OUTPUT_DIR=$2
OUTPUT_TF_FILE=$3
DATA=$4

source $REPO_ROOT/$COMMON_SCRIPTS_BASE/base_colors.sh

if [[ -z $DATA_DIR ]]; then
    echo_red '====> MUST specify the data folder! <===='
    exit 1
fi

if [[ -z $OUTPUT_DIR ]]; then
    echo_red '====> MUST specify the output folder! <===='
    exit 1
fi

if [[ -z $OUTPUT_TF_FILE ]]; then
    echo_red '====> MUST specify the Terraform output file name! <===='
    exit 1
fi

if [[ -z $DATA ]]; then
    DATA=data.yaml
fi

if [[ $OUTPUT_TF_FILE != *.tf ]]; then
    OUTPUT_TF_FILE=$3.tf
fi

echo
echo_yellow '====> Template generation started!!'
echo

# NOTE: Could add a for loop and look for glob of *.tf.j2 so it would not matter names...

echo_yellow '====> Generating main.tf ...'
$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/main.tf.j2 -o $OUTPUT_DIR/main.tf

echo_yellow '====> Generating outputs.tf ...'
$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/outputs.tf.j2 -o $OUTPUT_DIR/outputs.tf

echo_yellow '====> Generating variables.tf ...'
$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/variables.tf.j2 -o $OUTPUT_DIR/variables.tf

echo_yellow '====> Generating k8s_storage.tf ...'
$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/k8s_storage.tf.j2 -o $OUTPUT_DIR/k8s_storage.tf

echo_yellow '====> Generating locks.tf ...'
# This will generate the locks.tf.wait file where you will need to rename to locks.tf and run terraform apply again to apply the locks
$REPO_ROOT/bin/template_engine -d $DATA_DIR/$DATA -i $REPO_ROOT/$TEMPLATES_BASE/locks.tf.j2 -o $OUTPUT_DIR/locks.tf.wait

echo_yellow "====> Creating $OUTPUT_TF_FILE ..."
cat $OUTPUT_DIR/main.tf > $OUTPUT_DIR/$OUTPUT_TF_FILE
cat $OUTPUT_DIR/outputs.tf >> $OUTPUT_DIR/$OUTPUT_TF_FILE
cat $OUTPUT_DIR/variables.tf >> $OUTPUT_DIR/$OUTPUT_TF_FILE

echo_yellow '====> Removing temporary files ...'
rm $OUTPUT_DIR/main.tf
rm $OUTPUT_DIR/outputs.tf
rm $OUTPUT_DIR/variables.tf

echo
echo_green '====> Template generation completed!! <===='
echo
