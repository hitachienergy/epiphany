#!/bin/bash

SERVER_IP=$1;

curl -I -L $SERVER_IP/repos | grep "HTTP/1.1 200 OK";

sed -i -e "s/enabled=1/enabled=0/g" /etc/yum.repos.d/*.repo;

cat << EOF > /etc/yum.repos.d/epirepo.repo
[epirepo]
name=epirepo
baseurl=http://$SERVER_IP/repos/
enabled=1
gpgcheck=0
EOF

yum-config-manager --enable epirepo*;
yum makecache;
yum repolist;

