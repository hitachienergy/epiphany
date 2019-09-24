#!/bin/bash

EPIPHANY_FILES_LOCATION=$1;
OFFLINE_MODE=$2;
LOG_FILE=/root/script-execution.log;

WWW_SERVER_PATH=/var/www/html;

if $OFFLINE_MODE = true;
then
   rpm -i $EPIPHANY_FILES_LOCATION/offline_prereqs/*.rpm;
else
   yum install -y httpd createrepo yum-utils;
fi

mv $EPIPHANY_FILES_LOCATION/* $WWW_SERVER_PATH;

setenforce 0;
systemctl start httpd;

createrepo $REPOSITORY_PATH;
