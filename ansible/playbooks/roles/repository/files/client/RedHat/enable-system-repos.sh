#!/bin/bash -eu

REPOS_LIST_FILE=/var/tmp/enabled-system-repos.txt

readarray -t repos < $REPOS_LIST_FILE

for repo in "${repos[@]}"; do
  echo "Enabling repository: $repo"
  dnf config-manager --set-enabled "$repo"
done
