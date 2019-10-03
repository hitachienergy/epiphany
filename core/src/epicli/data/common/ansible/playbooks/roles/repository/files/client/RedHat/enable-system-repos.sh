#!/bin/bash -eu

REPOS_LIST_FILE=/tmp/enabled-system-repos.txt

cat $REPOS_LIST_FILE | while read repository
do
  echo "Enabling repository: $repository"
  yum-config-manager --enable $repository
done
