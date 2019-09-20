#!/bin/bash

PACKAGE_LIST=$(cat $1)
LOG_FILE=/root/script-execution.log

WWW_SERVER_PATH=/var/www/html;

REPOSITORY_PATH=$WWW_SERVER_PATH/repos;
FILES_PATH=$WWW_SERVER_PATH/files;
IMAGES_PATH=$WWW_SERVER_PATH/images;

mkdir -p $WWW_SERVER_PATH;
mkdir -p $REPOSITORY_PATH;
mkdir -p $FILES_PATH;
mkdir -p $IMAGES_PATH;

yum install -y httpd createrepo  yum-utils;

for package in $PACKAGE_LIST ; do
        echo "========== $package =========" | tee $LOG_FILE;
        repoquery -a --qf  '%{ui_nevra}' $package;
        repoquery -a --qf  '%{ui_nevra}' $package | xargs yumdownloader --destdir $REPOSITORY_PATH | tee $LOG_FILE;
        echo "========== $package - dependencies =========" | tee $LOG_FILE;
        repoquery -R --resolve -a --qf  '%{ui_nevra}' $package;
        repoquery -R --resolve -a --qf  '%{ui_nevra}' $package | xargs yumdownloader --destdir $REPOSITORY_PATH | tee $LOG_FILE;
done

setenforce 0;
systemctl start httpd;

createrepo $REPOSITORY_PATH;


