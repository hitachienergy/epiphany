#!/bin/bash -eu

epi_repo_server_path=$1 # /var/www/html/epirepo is the default
is_offline_mode=$2 # true/false
apt_repo_path="/etc/apt/sources.list"

apt_update() {
  echo "Updating list of available packages..."
  apt -y update
}

# params: <repo_path>
generate_repo_metadata() {
  local repo_path="$1"

  echo "Generating repository metadata..."
  # 'cd' is needed here because 'dpkg-scanpackages' prepends path to "Filename" field in Packages.gz
  # otherwise it would break package URL for apt
  # -m is important because it allows same packages with different versions
  cd "${repo_path}/packages" \
  && /var/tmp/epi-repository-setup-scripts/dpkg-scanpackages -m . | gzip -9c > Packages.gz
}

install_apache() {
  echo "Installing apache2 package..."
  # force non-interactive mode, ref: https://bugs.launchpad.net/ubuntu/+source/ansible/+bug/1833013
  DEBIAN_FRONTEND=noninteractive \
  UCF_FORCE_CONFOLD=1 \
    apt-get \
    -o Dpkg::Options::=--force-confold \
    -o Dpkg::Options::=--force-confdef \
    -y -q install apache2
}


if [[ "$is_offline_mode" == "true" ]]; then
  # bootstrap apache installation in air-gap mode
  if [[ -f $apt_repo_path ]]; then
      echo "Disabling default repositories..."
      mv $apt_repo_path ${apt_repo_path}.bak
  fi

  if ! dpkg -l | grep -q "^ii  libdpkg-perl\s"; then
    echo "Package libdpkg-perl not found, installing..."
    dpkg -i "${epi_repo_server_path}"/packages/libdpkg-perl*.deb
    retval=$?
    if [[ $retval -ne "0" ]]; then
      echo "Exiting..."
      exit "$retval"
    fi
  fi

  generate_repo_metadata "$epi_repo_server_path"
  echo "deb [trusted=yes] file:${epi_repo_server_path}/packages ./" > /etc/apt/sources.list.d/epilocal.list
  apt_update
  install_apache
  echo "Removing temporary repo definition: /etc/apt/sources.list.d/epilocal.list..."
  rm -f /etc/apt/sources.list.d/epilocal.list
  apt_update
else
  # online mode
  install_apache
  generate_repo_metadata "$epi_repo_server_path"
fi

systemctl start apache2
