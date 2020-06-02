#!/bin/bash

if ls /usr/local/share/ca-certificates/*.crt 1> /dev/null 2>&1; then
  pattern="/usr/local/share/ca-certificates/*.crt"
  files=( $pattern )
  for i in "${files[@]}"
  do
    chmod 644 $i
  done
  if ls /*.pem 1> /dev/null 2>&1; then
    pattern="/*.pem"
    files=( $pattern )
    f="${files[0]}"
    echo "Setting PIP ca-bundle $f"
    chmod 644 $f
    pip config set global.cert $f
    pip config list
  else 
    f="${files[0]}"
    echo "Setting PIP cert $f"
    pip config set global.cert $f
    pip config list
  fi
  update-ca-certificates
else
  echo "No cert/ca-bundle to setup"
fi

