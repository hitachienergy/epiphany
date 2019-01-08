#!/bin/bash
#
# Copyright 2018, LambdaStack
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Colors
# Black        0;30     Dark Gray     1;30
# Red          0;31     Light Red     1;31
# Green        0;32     Light Green   1;32
# Brown/Orange 0;33     Yellow        1;33
# Blue         0;34     Light Blue    1;34
# Purple       0;35     Light Purple  1;35
# Cyan         0;36     Light Cyan    1;36
# Light Gray   0;37     White         1;37

# NB: Color constants
BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
LIGHT_GRAY='\033[0;37m'
DARK_GRAY='\033[1;30m'
LIGHT_RED='\033[1;31m'
LIGHT_GREEN='\033[1;32m'
YELLOW='\033[1;33m'
LIGHT_BLUE='\033[1;34m'
LIGHT_PURPLE='\033[1;35m'
LIGHT_CYAN='\033[1;36m'
WHITE='\033[1;37m'

# NB: Make sure to change color back to ${NC} so that user's terminal stays with the last color used.
NC='\033[0m' # No Color

# NB: Functions that echo out color...

function echo_print {
    color=$1
    text=$2
    echo -e "${color}$text${NC}"
}

function echo_black {
    echo_print $BLACK "$1"
}

function echo_red {
    echo_print $RED "$1"
}

function echo_green {
    echo_print $GREEN "$1"
}

function echo_orange {
    echo_print $ORANGE "$1"
}

function echo_blue {
    echo_print $BLUE "$1"
}

function echo_purple {
    echo_print $PURPLE "$1"
}

function echo_cyan {
    echo_print $CYAN "$1"
}

function echo_light_gray {
    echo_print $LIGHT_GRAY "$1"
}

function echo_dark_gray {
    echo_print $DARK_GRAY "$1"
}

function echo_light_red {
    echo_print $LIGHT_RED "$1"
}

function echo_light_green {
    echo_print $LIGHT_GREEN "$1"
}

function echo_yellow {
    echo_print $YELLOW "$1"
}

function echo_light_blue {
    echo_print $LIGHT_BLUE "$1"
}

function echo_light_purple {
    echo_print $LIGHT_PURPLE "$1"
}

function echo_light_cyan {
    echo_print $LIGHT_CYAN "$1"
}

function echo_white {
    echo_print $WHITE "$1"
}
