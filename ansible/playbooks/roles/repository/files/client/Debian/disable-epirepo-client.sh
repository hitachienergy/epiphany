#!/bin/bash -eu

rm -f /etc/apt/sources.list.d/epirepo.list
apt-get clean
apt update