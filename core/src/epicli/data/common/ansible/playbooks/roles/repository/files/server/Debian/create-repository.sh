#!/bin/bash -eu

epi_repo_server_path=$1 # /var/www/html/epirepo is the default
is_offline_mode=$2 # true/false
script_path=$(cd "$(dirname "$0")"; pwd -P)
apt_repo_path="/etc/apt/sources.list"


if [[ "$is_offline_mode" == "true" ]]; then
  # bootstrap apache and dpkg-dev installation in air-gap mode
  if [[ -f $apt_repo_path ]]; then
      echo "Disabling default repositories..."
      mv $apt_repo_path ${apt_repo_path}.bak
  fi

  if ! dpkg -l | grep -q "^ii  libdpkg-perl\s"; then 
    echo "Package libdpkg-perl not found, installing..."
    dpkg -i "${epi_repo_server_path}/packages/libdpkg-perl*.deb"
    retval=$?
    [[ $retval -eq "0" ]] || echo "Exiting.." && exit "$retval"
  fi

  echo "Generating repository metadata..."
  cd "${epi_repo_server_path}/packages" && /tmp/epi-repository-setup-scripts/dpkg-scanpackages -m . | gzip -9c > Packages.gz && cd "${script_path}"
  echo "deb [trusted=yes] file:${epi_repo_server_path}/packages ./" > /etc/apt/sources.list.d/epilocal.list
  #apt update --assume-no # workaround for botched docker repository https://github.com/docker/for-linux/issues/812
  echo "Updating list of available packages..."
  apt -y update
  echo "Installing apache..."
  # force non-interactive mode, ref: https://bugs.launchpad.net/ubuntu/+source/ansible/+bug/1833013
  DEBIAN_FRONTEND=noninteractive \
  UCF_FORCE_CONFOLD=1 \
    apt-get \
    -o Dpkg::Options::=--force-confold \
    -o Dpkg::Options::=--force-confdef \
    -y -q install apache2 dpkg-dev
  echo "Removing temporary repo definition: /etc/apt/sources.list.d/epilocal.list..."
  rm -f /etc/apt/sources.list.d/epilocal.list
  #rm -f ${epi_repo_server_path}/packages/Packages.gz
  echo "Updating list of available packages..."
  apt -y update
else
  # for online mode just install apache
  echo "Installing apache2 package"
  # force non-interactive mode, ref: https://bugs.launchpad.net/ubuntu/+source/ansible/+bug/1833013
  DEBIAN_FRONTEND=noninteractive \
  UCF_FORCE_CONFOLD=1 \
    apt-get \
    -o Dpkg::Options::=--force-confold \
    -o Dpkg::Options::=--force-confdef \
    -y -q install apache2 dpkg-dev

  # -m is important because it allow same packages with different versions
  # 'cd' is needed here becuase 'dpkg-scanpackages' prepends path to "Filename" field in Packages.gz
  # otherwise it would break package URL for apt
  cd "${epi_repo_server_path}/packages" && /tmp/epi-repository-setup-scripts/dpkg-scanpackages -m . | gzip -9c > Packages.gz && cd "${script_path}"
fi

systemctl start apache2
