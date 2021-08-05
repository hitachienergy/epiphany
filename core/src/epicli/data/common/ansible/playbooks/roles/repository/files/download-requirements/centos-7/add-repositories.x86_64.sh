#!/usr/bin/env bash -eu

CENTOS_EXTRAS=$(cat <<'EOF'
[centos-extras]
name=Centos extras - x86_64
baseurl=http://mirror.centos.org/centos/7/extras/x86_64
enabled=1
gpgcheck=1
gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-7
EOF
)

add_repo_as_file 'centos-extras' "$CENTOS_EXTRAS" # for Docker dependencies
add_repo_from_script 'https://dl.2ndquadrant.com/default/release/get/10/rpm' # for repmgr
disable_repo '2ndquadrant-dl-default-release-pg10-debug' # script adds 2 repositories, only 1 is required
