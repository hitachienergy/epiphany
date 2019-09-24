#!/bin/bash

SERVER_IP=$1;
DATE=`date +%Y.%m.%d-%H.%M.%S`;

curl -I -L $SERVER_IP/repos | grep "HTTP/1.1 200 OK";

cp /etc/apt/sources.list /etc/apt/sources.list.bak_$DATE;
echo "deb [trusted=yes] http://$SERVER_IP/repos/ bionic main" > /etc/apt/sources.list;

apt-cache policy;

apt update;

