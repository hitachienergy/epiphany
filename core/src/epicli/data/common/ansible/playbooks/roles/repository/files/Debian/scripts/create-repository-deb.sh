#!/bin/bash

PACKAGE_LIST=$(cat /root/deb-package-list.txt)
DOWNLOAD_DIRECTORY=/root/packages
LOG_FILE=/root/script-execution.log

WWW_SERVER_PATH=/var/www/html;

REPOSITORY_PATH=$WWW_SERVER_PATH/repos;
FILES_PATH=$WWW_SERVER_PATH/files;
IMAGES_PATH=$WWW_SERVER_PATH/images;

apt install -y apache2 reprepro;
systemctl start apache2
apt clean;


mkdir -p $REPOSITORY_PATH;
mkdir -p $REPOSITORY_PATH/conf;

cat << EOF > $REPOSITORY_PATH/conf/distributions 
Origin: epiphany.offline.repo
Label: epiphany.offline.repo
Codename: bionic
Architectures: i386 amd64
Components: main restricted universe multiverse
Description: Epiphany Offline Repository
EOF

for package in $PACKAGE_LIST ; do
	echo "$package:" | tee $LOG_FILE;
	apt-get install -y  --download-only $package | tee $LOG_FILE ;
done

reprepro --basedir $REPOSITORY_PATH includedeb bionic /var/cache/apt/archives/*.deb;

