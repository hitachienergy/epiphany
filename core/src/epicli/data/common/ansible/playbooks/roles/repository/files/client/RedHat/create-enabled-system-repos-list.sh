#!/bin/bash -eu

ENABLED_REPOS_FILE=/var/tmp/enabled-system-repos.txt

if [ ! -f "$ENABLED_REPOS_FILE" ]; then
  yum repolist enabled | awk '/^$/ {next}; /repo id/ {f=1; next}; /^repolist/ {f=0}; f {sub(/\/.*/,""); print $1}' > $ENABLED_REPOS_FILE
fi
