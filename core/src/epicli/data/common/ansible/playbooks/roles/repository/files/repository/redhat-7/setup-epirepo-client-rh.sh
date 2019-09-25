#!/bin/bash

SERVER_IP=$1;

curl -I -L $SERVER_IP/repos | grep "HTTP/1.1 200 OK";

# Todo: remove if unnecessary
#sed -i -e "s/enabled=1/enabled=0/g" /etc/yum.repos.d/*.repo;

cat << EOF > /etc/yum.repos.d/epirepo.repo
[epirepo]
name=epirepo
baseurl=http://$SERVER_IP/packages/
enabled=1
gpgcheck=0
EOF

yum-config-manager --enable epirepo*;
yum makecache;
yum repolist;

