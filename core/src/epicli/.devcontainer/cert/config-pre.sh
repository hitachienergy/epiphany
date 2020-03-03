#!/bin/bash

if ls /usr/local/share/ca-certificates/*.crt 1> /dev/null 2>&1; then
  echo "Setup cert for System, PIP..."
  pattern="/usr/local/share/ca-certificates/*.crt"
  files=( $pattern )
  f="${files[0]}"
  echo "Processing cert $f"
  chmod 644 $f
  pip config set global.cert $f
  pip config list
  update-ca-certificates
else
     echo "No cert to setup"
fi

