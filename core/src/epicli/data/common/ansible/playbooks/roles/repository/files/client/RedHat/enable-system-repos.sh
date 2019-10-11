#!/bin/bash -eu

REPOS_LIST_FILE=/var/tmp/enabled-system-repos.txt
YUM_REPOS_BACKUP_FILE=/etc/yum.repos.d/yum.repos.d-epi-backup.tar

if [ -f $YUM_REPOS_BACKUP_FILE ]; then # hosts without yum-config-manager
  echo "Restoring /etc/yum.repos.d/*.repo from: $YUM_REPOS_BACKUP_FILE"
  if tar -xv --file $YUM_REPOS_BACKUP_FILE --directory /etc/yum.repos.d \
         --strip-components=2 etc/yum.repos.d/*.repo; then
    echo "yum repositories restored"
    rm -f $YUM_REPOS_BACKUP_FILE
  else
    echo "Extracting tar failed: $YUM_REPOS_BACKUP_FILE"
    exit 2
  fi
else # hosts with yum-config-manager
  cat $REPOS_LIST_FILE | while read repository
  do
    echo "Enabling repository: $repository"
    yum-config-manager --enable $repository
  done
fi