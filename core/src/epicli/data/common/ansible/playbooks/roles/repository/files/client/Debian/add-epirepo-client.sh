#!/bin/bash

REPOSITORY_URL=$1

echo "deb [trusted=yes] $REPOSITORY_URL/packages ./" > /etc/apt/sources.list.d/epirepo.list

apt-cache policy

apt update