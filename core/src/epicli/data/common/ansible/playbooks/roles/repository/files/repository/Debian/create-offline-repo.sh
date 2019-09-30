#!/bin/bash

# before execute install apache2

mkdir -p /var/www/html/epirepo/packages
cp /var/cache/apt/archives/* /var/www/html/epirepo/packages/

# -m is important because it allow same packages with different versions
dpkg-scanpackages -m /var/www/html/epirepo/packages | gzip -9c > /var/www/html/epirepo/packages/Packages.gz

apt update