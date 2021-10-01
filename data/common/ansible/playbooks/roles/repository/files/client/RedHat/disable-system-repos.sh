#!/bin/bash -eu

REPOS_LIST_FILE=/var/tmp/enabled-system-repos.txt
YUM_REPOS_BACKUP_FILE=/etc/yum.repos.d/yum.repos.d-epi-backup.tar

if yum-config-manager --version > /dev/null 2>&1; then
  cat $REPOS_LIST_FILE | while read repository
  do
    echo "Disabling repository: $repository"
    yum-config-manager --disable $repository
  done
elif [ ! -f $YUM_REPOS_BACKUP_FILE ]; then # for hosts where yum-utils is not available
  echo "Disabling all yum repositories by backup & remove files in /etc/yum.repos.d"
  tar -cv --verify --directory="/" --file=$YUM_REPOS_BACKUP_FILE /etc/yum.repos.d &&
  rm -f /etc/yum.repos.d/*.repo
fi