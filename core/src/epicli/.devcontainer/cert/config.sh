#!/bin/bash
FILES=/usr/local/share/ca-certificates/*.crt
for f in $FILES
do
  echo "Processing cert $f..."
  chmod 644 $f
  pip config set global.cert $f
done
pip config list
update-ca-certificates