#!/bin/bash -eu

EPI_REPO_SERVER_PATH=$1 # /var/www/html/epirepo is the default
IS_OFFLINE_MODE=$2

if $IS_OFFLINE_MODE = true; then
  echo yum install -y $(ls $EPI_REPO_SERVER_PATH/packages/offline_prereqs/*.rpm) #TODO: to rewrite for ubuntu
else
  apt -y install reprepro apache2 dpkg-dev
fi

systemctl start apache2

# -m is important because it allow same packages with different versions
# 'cd' is needed here becuase 'dpkg-scanpackages' prepends path to "Filename" field in Packages.gz, otherwise it would break package URL for apt
cd /var/www/html/epirepo/packages && dpkg-scanpackages -m . | gzip -9c > Packages.gz