#!/bin/bash -eu

epi_repo_server_path=$1 # /var/www/html/epirepo is the default
is_offline_mode=$2

if [[ "$is_offline_mode" == "true" ]]; then
  # deprecated 'yum localinstall' is used since 'yum install' returns error code when 'nothing to do'
  yum --cacheonly --disablerepo='*' localinstall -y $(ls "${epi_repo_server_path}"/packages/repo-prereqs/*.rpm)
else
  # fix for RHEL 7.6 and 7.7 (#1108): httpd (2.4.6-93) requires httpd-tools = 2.4.6-93 but latest available is 2.4.6-90
  if [[ ! $(yum install -y httpd createrepo yum-utils) ]]; then
    echo -e "\nWARN: 'yum install -y httpd createrepo yum-utils' FAILED"
    echo -e "INFO: Retrying with fixed version (httpd-2.4.6-90.el7)...\n"
    yum install -y httpd-2.4.6-90.el7 createrepo yum-utils
  fi
fi

systemctl start httpd

createrepo "${epi_repo_server_path}/packages"
