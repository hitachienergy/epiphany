#!/bin/bash -eu

REPOS_BACKUP_FILE=/var/tmp/enabled-system-repos.tar

if [ -f "$REPOS_BACKUP_FILE" ]; then
  rm -f /etc/apt/sources.list /etc/apt/sources.list.d/*
else
  echo "${REPOS_BACKUP_FILE} file not found. You don't seem to have a backup of the repositories. Cowardly refusing to delete system files."
fi
