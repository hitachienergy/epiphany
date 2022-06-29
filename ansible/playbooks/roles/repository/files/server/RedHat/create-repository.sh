#!/bin/bash -eu

epi_repo_server_path=$1 # /var/www/html/epirepo is the default
is_offline_mode=$2

if [[ "$is_offline_mode" == "true" ]]; then
  if dnf list installed python3-createrepo_c; then  # install all
    readarray -t prereq_packages < <(find "${epi_repo_server_path}/packages/repo-prereqs/" -type f -name \*.rpm)
  else  # skip python3-createrepo_c
    readarray -t prereq_packages < <(find "${epi_repo_server_path}/packages/repo-prereqs/" -type f -name \*.rpm \
                                          ! -name python3-createrepo_c\*)
  fi
  dnf localinstall --cacheonly --disablerepo='*' -y "${prereq_packages[@]}"
else
  dnf install -y httpd createrepo
fi

systemctl start httpd

createrepo "${epi_repo_server_path}/packages"
