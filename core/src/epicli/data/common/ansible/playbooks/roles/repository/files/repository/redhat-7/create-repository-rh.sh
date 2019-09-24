#!/bin/bash

EPIPHANY_REQUIREMENTS_PATH=$1;
IS_OFFLINE_MODE=$2;
LOG_FILE=/root/script-execution.log;

WWW_SERVER_PATH=/var/www/html;

REPOSITORY_PATH=$WWW_SERVER_PATH/packages;
FILES_PATH=$WWW_SERVER_PATH/files;
IMAGES_PATH=$WWW_SERVER_PATH/images;

mkdir -p $REPOSITORY_PATH;
mkdir -p $FILES_PATH;
mkdir -p $IMAGES_PATH;

if $IS_OFFLINE_MODE = true;
then
   yum install -y `ls $EPIPHANY_REQUIREMENTS_PATH/packages/offline_prereqs/*.rpm`;
else
   yum install -y httpd createrepo yum-utils;
fi

mv $EPIPHANY_REQUIREMENTS_PATH/* $WWW_SERVER_PATH;

setenforce 0;
systemctl start httpd;

createrepo $REPOSITORY_PATH;
