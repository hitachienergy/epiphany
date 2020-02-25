#!/bin/bash
if ls /usr/local/share/ca-certificates/*.crt 1> /dev/null 2>&1; then
  echo "Setup cert for Ansible, AWS..."
  pattern="/usr/local/share/ca-certificates/*.crt"
  files=( $pattern )
  f="${files[0]}"
  mkdir "/home/vscode/.aws/"
  echo -e "[defaults]\ntimeout=0" >> "/home/vscode/.ansible.cfg"
  echo -e "[default]\nca_bundle=$f" >> "/home/vscode/.aws/config"
else
     echo "No cert to setup"
fi

