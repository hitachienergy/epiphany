#!/bin/bash -eu

ENABLED_REPOS_LIST_FILE=/var/tmp/enabled-system-repos.txt

if [ ! -f "$ENABLED_REPOS_LIST_FILE" ]; then
  # 'yum repoinfo' or 'yum repolist -v' not used since they may require Internet access, even with --cacheonly
  yum --cacheonly repolist enabled | awk '/^$/ {next}; /repo id/ {f=1; next}; /^repolist/ {f=0}; f {sub(/\/.*/,""); print $1}' | tr -d '!' > $ENABLED_REPOS_LIST_FILE
fi
