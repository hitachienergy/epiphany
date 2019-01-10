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

# NB: source these common functions early in your scripts
# MUST pass in a valid path to base_colors.sh

SCRIPT_DIR=$1

source $SCRIPT_DIR/base_colors.sh

function show_help {
    echo
    echo_green "Usage: ./epiphany [options]"
    echo
    echo_green "Epiphany will build the infrastructure for environments that are the control of Epiphany and use "
    echo_green "the environments provided by the customer."
    echo
    echo_green "Epiphany is the full automation of Kubernetes and Docker for microservices "
    echo_green "platform. It can run on a single node (laptop) or a large cluster. It allows the developer "
    echo_green "to have a delivery platform that is common on all of the platforms we and/or our customers "
    echo_green "use such as 'Azure', 'AWS', 'Bare-metal', 'VBox' and 'VMWare'."
    echo
    echo_green "Options:"
    echo_green "    -b  (required/optional) Builds out Epiphany on the given infrastructure. If specified without -i option then it is assumed the infrastructure has already been bootstrapped with OS, IPs, Gateways and SSH Keys. If specified with -i then the infrastructure will be built out first then Epiphany (assuming the given platform supports being built out)"
    echo_green "    -d  (optional) Base data path (i.e., /mypath/data). Defaults to <repo root>/data. "
    echo_green "                   Full path is generated with -p and -f"
    echo_green "    -e  (optional) Environment (i.e., dev, qa, staging, prod). Defaults to dev"
    echo_green "    -f  (optional) Sub-folder where data resides (i.e., infrastructure/epiphany). Defaults to infrastructure/epiphany"
    echo_green "    -g  (optional) Gets the prerequisites only. Use it with -r to remove existing prerequisites first"
    echo_green "    -i  (optional/required) Builds out the infrastructure only or first. If the given infrastructure does not already exists then by specifing -i will build it out (assuming the given environment supports being built out)"
    echo_green "    -o  (optional) Base output directory. Defaults to <repo root>/build. Full path is generated with -p and -f"
    echo_green "    -p  (optional) Platform. Defaults to 'azure'. Valid options are aws, azure, metal, vbox and vmware"
    echo_green "more..."
    echo
    echo_yellow "Examples: (data.yaml and manifest.yaml) files must exist depending on environment"
    echo_yellow "   ./epiphany -i"
    echo_yellow "       Builds out the infrastructure only if the given platform supports it. This option "
    echo_yellow "       requires a data.yaml file that contains the platform specific data (i.e., Azure, AWS)."
    echo
    echo_yellow "   ./epiphany -b"
    echo_yellow "       Builds out Epiphany on the existing infrastructure. This option requires manifest.yaml "
    echo_yellow "       to be present in the default or specified directory. If on Azure or any environment "
    echo_yellow "       that creates an infrastructure this data file will be automatically created. If on a "
    echo_yellow "       controlled by the customer then you will have to build the file with information from "
    echo_yellow "       the customer."
    echo
    echo_yellow "   ./epiphany -b -i"
    echo_yellow "       Builds out the infrastructure and then Epiphany on that infrastructure. This assumes "
    echo_yellow "       the given platform supports being built out."
    echo
    echo_yellow "   ./epiphany -i -f infrastructure/myplatform"
    echo_yellow "       The -f option will override the default of infrastructure/epiphany as the sub-folder "
    echo_yellow "       of where the data.yaml will be fulled from."
    echo
}
