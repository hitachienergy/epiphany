#!/bin/bash -eu

REPOS_LIST_FILE=/var/tmp/enabled-system-repos.txt

readarray -t repos < $REPOS_LIST_FILE

for repo in "${repos[@]}"; do
  echo "Disabling repository: $repo"
  dnf config-manager --set-disabled "$repo"
done
