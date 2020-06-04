#!/bin/bash
if ls /usr/local/share/ca-certificates/*.crt 1> /dev/null 2>&1; then
  mkdir "/home/vscode/.aws/"
  if ls /*.pem 1> /dev/null 2>&1; then
    pattern="/*.pem"
    files=( $pattern )
    f="${files[0]}"
    echo "Setup AWS ca-bundle $f"
    echo -e "[default]\nca_bundle=$f" >> "/home/vscode/.aws/config"
  else 
    pattern="/usr/local/share/ca-certificates/*.crt"
    files=( $pattern )
    f="${files[0]}"
    echo "Setup AWS cert $f"
    echo -e "[default]\nca_bundle=$f" >> "/home/vscode/.aws/config"
  fi
else
  echo "No cert/ca-bundle to setup"
fi

