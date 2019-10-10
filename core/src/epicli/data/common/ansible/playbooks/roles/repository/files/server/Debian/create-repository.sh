#!/bin/bash -eu

EPI_REPO_SERVER_PATH=$1 # /var/www/html/epirepo is the default
IS_OFFLINE_MODE=$2

if $IS_OFFLINE_MODE = true; then
    # bootstrap apache and dpkg-dev installation in air-gap mode
    if ! dpkg -l | grep -q libdpkg-perl; then
        echo libdpkg-perl not found, installing...
        dpkg -i ${EPI_REPO_SERVER_PATH}/packages/libdpkg-perl*.deb
    fi
    cd ${EPI_REPO_SERVER_PATH}/packages && /tmp/epi-repository-setup-scripts/dpkg-scanpackages -m . | gzip -9c > Packages.gz && cd -
    echo "deb [trusted=yes] file:${EPI_REPO_SERVER_PATH}/packages ./" > /etc/apt/sources.list.d/epilocal.list
    apt update --assume-no # workaround for botched docker repository https://github.com/docker/for-linux/issues/812
    apt -y install apache2 dpkg-dev
    rm -f /etc/apt/sources.list.d/epilocal.list
    rm -f ${EPI_REPO_SERVER_PATH}/packages/Packages.gz
    apt update --assume-no
else
    apt -y install apache2 dpkg-dev
fi

systemctl start apache2

# -m is important because it allow same packages with different versions
# 'cd' is needed here becuase 'dpkg-scanpackages' prepends path to "Filename" field in Packages.gz, otherwise it would break package URL for apt
cd /var/www/html/epirepo/packages && dpkg-scanpackages -m . | gzip -9c > Packages.gz
