#!/bin/bash -eu

EPI_REPO_SERVER_PATH=$1 # /var/www/html/epirepo is the default
IS_OFFLINE_MODE=$2

if $IS_OFFLINE_MODE = true; then
  # deprecated 'yum localinstall' is used since 'yum install' returns error code when 'nothing to do'
  yum --cacheonly --disablerepo='*' localinstall -y $(ls $EPI_REPO_SERVER_PATH/packages/repo-prereqs/*.rpm)
else
  yum install -y httpd createrepo yum-utils
fi

systemctl start httpd

createrepo $EPI_REPO_SERVER_PATH/packages

if systemctl is-active firewalld; then
  firewall-cmd --permanent --add-service=http
  firewall-cmd --reload
fi
