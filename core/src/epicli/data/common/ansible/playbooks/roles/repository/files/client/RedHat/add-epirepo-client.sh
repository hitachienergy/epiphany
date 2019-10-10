#!/bin/bash -eu

REPOSITORY_URL=$1

CURL_CMD="curl --head --location --connect-timeout 30 --silent --show-error $REPOSITORY_URL"
CURL_OUTPUT=$($CURL_CMD 2>&1) || { echo "Command failed: $CURL_CMD"; echo "Output was: $CURL_OUTPUT"; exit 2; }

egrep 'HTTP/.{1,3} 200 OK' <<< "$CURL_OUTPUT" || { echo "HTTP 200 status code not found"; exit 3; }

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