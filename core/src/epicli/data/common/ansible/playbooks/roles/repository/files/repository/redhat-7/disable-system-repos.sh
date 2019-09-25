#!/bin/bash
REPOS_LIST_FILE=/tmp/enabled-system-repos.txt

cat $REPOS_LIST_FILE | while read line
do
  echo $line;
  yum-config-manager --disable $line;
done

