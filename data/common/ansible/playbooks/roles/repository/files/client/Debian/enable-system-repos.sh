#!/bin/bash -eu

REPOS_BACKUP_FILE=/var/tmp/enabled-system-repos.tar

tar -C / --absolute-name -xvf ${REPOS_BACKUP_FILE} 2>&1