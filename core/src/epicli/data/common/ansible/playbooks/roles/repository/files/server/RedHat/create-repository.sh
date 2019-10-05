#!/bin/bash -eu

EPI_REPO_SERVER_PATH=$1 # /var/www/html/epirepo is the default
IS_OFFLINE_MODE=$2

if $IS_OFFLINE_MODE = true; then
  yum install -y $(ls $EPI_REPO_SERVER_PATH/packages/repo_prereqs/*.rpm) #TODO: to test
else
  yum install -y httpd createrepo yum-utils
fi

setenforce 0
systemctl start httpd

createrepo $EPI_REPO_SERVER_PATH/packages