#!/bin/bash

SERVER_IP=$1;

echo "deb [trusted=yes] http://$SERVER_IP/epirepo/ packages/" > /etc/apt/sources.list.d/epirepo.list;

apt-cache policy;

apt update;