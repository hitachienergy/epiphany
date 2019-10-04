#!/bin/bash

REPOSITORY_URL=$1

echo "deb [trusted=yes] $REPOSITORY_URL/packages ./" > /etc/apt/sources.list.d/epirepo.list

apt-cache policy

apt update



# #!/bin/bash -eu

# REPOSITORY_URL=$1

# curl -I -L $REPOSITORY_URL | grep "HTTP/1.1 200 OK"

# cat << EOF > /etc/yum.repos.d/epirepo.repo
# [epirepo]
# name=epirepo
# baseurl=$REPOSITORY_URL/packages/
# enabled=1
# gpgcheck=0
# EOF

# yum-config-manager --enable epirepo
# yum makecache
# yum repolist
