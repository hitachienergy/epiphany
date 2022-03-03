#!/bin/bash -eu

epi_repo_server_path=$1 # /var/www/html/epirepo is the default
is_offline_mode=$2

if [[ "$is_offline_mode" == "true" ]]; then
  dnf localinstall --cacheonly --disablerepo='*' -y $(ls "${epi_repo_server_path}"/packages/repo-prereqs/*.rpm)
else
  dnf install -y httpd createrepo
fi

systemctl start httpd

createrepo "${epi_repo_server_path}/packages"
