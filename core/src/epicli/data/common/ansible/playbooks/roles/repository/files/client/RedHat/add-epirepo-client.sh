#!/bin/bash -eu

REPOSITORY_URL=$1

curl -I -L $REPOSITORY_URL | grep "HTTP/1.1 200 OK"

cat << EOF > /etc/yum.repos.d/epirepo.repo
[epirepo]
name=epirepo
baseurl=$REPOSITORY_URL/packages/
enabled=1
gpgcheck=0
EOF

yum-config-manager --enable epirepo
yum makecache fast
yum repolist