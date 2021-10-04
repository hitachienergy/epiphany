#!/bin/bash -eu

REPOS_BACKUP_FILE=/var/tmp/enabled-system-repos.tar

if [ ! -f "$REPOS_BACKUP_FILE" ]; then
  tar --ignore-failed-read --absolute-names -cvpf ${REPOS_BACKUP_FILE} /etc/apt/sources.list /etc/apt/sources.list.d/ 2>&1
fi
