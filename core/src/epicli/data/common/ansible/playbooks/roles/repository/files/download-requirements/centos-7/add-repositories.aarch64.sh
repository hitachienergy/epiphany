#!/usr/bin/env bash -eu

CENTOS_EXTRAS=$(cat <<'EOF'
[centos-extras]
name=Centos extras - aarch64
baseurl=http://mirror.centos.org/altarch/7/extras/aarch64
enabled=1
gpgcheck=1
gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-7
EOF
)

add_repo_as_file 'centos-extras' "$CENTOS_EXTRAS" # for Docker dependencies
