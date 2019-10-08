#!/bin/bash -eu

REPOS_LIST_FILE=/var/tmp/enabled-system-repos.txt

cat $REPOS_LIST_FILE | while read repository
do
  echo "Disabling repository: $repository"
  yum-config-manager --disable $repository
done