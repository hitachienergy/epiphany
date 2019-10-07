#!/bin/bash -eu

EPI_REPO_SERVER_PATH=$1 # /var/www/html/epirepo is the default
IS_OFFLINE_MODE=$2

if $IS_OFFLINE_MODE = true; then
  echo yum install -y $(ls $EPI_REPO_SERVER_PATH/packages/offline_prereqs/*.rpm) #TODO: to rewrite for ubuntu
else
  apt -y install reprepro apache2 dpkg-dev
fi

systemctl start apache2

# -m is important because it allow same packages with different versions
# cd is needed here becuase dpkg-scanpackages prepends path to "Filename" field in Packages.gz
# and consequently breaks package URL
cd /var/www/html/epirepo/packages && dpkg-scanpackages -m . | gzip -9c > Packages.gz





# #!/bin/bash

# # before execute install apache2

# mkdir -p /var/www/html/epirepo/packages
# cp /var/cache/apt/archives/* /var/www/html/epirepo/packages/

# # -m is important because it allow same packages with different versions
# dpkg-scanpackages -m /var/www/html/epirepo/packages | gzip -9c > /var/www/html/epirepo/packages/Packages.gz

# apt update