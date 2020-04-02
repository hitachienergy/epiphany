#!/bin/bash -eu

EPI_REPO_SERVER_PATH=$1 # /var/www/html/epirepo is the default
IS_OFFLINE_MODE=$2

if $IS_OFFLINE_MODE = true; then
  # deprecated 'yum localinstall' is used since 'yum install' returns error code when 'nothing to do'
  yum --cacheonly --disablerepo='*' localinstall -y $(ls $EPI_REPO_SERVER_PATH/packages/repo-prereqs/*.rpm)
else
  # fix for RHEL 7.6 and 7.7 (#1108): httpd (2.4.6-93) requires httpd-tools = 2.4.6-93 but latest available is 2.4.6-90
  if ! yum install -y httpd createrepo yum-utils; then
    echo
    echo "WARN: 'yum install -y httpd createrepo yum-utils' FAILED"
    echo "INFO: Retrying with fixed version (httpd-2.4.6-90.el7)..."
    echo
    yum install -y httpd-2.4.6-90.el7 createrepo yum-utils
  fi
fi

systemctl start httpd

createrepo $EPI_REPO_SERVER_PATH/packages
