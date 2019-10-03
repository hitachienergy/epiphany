#!/bin/bash -eu

ENABLED_REPOS_FILE=/tmp/enabled-system-repos.txt

if [ ! -f "$ENABLED_REPOS_FILE" ]; then
  yum repolist -v enabled | grep -i Repo-id | awk -F ":" '{print $2}' |  sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' | awk -F "/" '{print $1}' > $ENABLED_REPOS_FILE
fi
