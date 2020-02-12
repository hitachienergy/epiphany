#!/bin/bash
FILES=/usr/local/share/ca-certificates/*.crt

if [ ${#FILES[@]} -gt 0 ]
then
  echo "Processing cert ${FILES[0]}..."
  chmod 644 ${FILES[0]}
  pip config set global.cert ${FILES[0]}
  pip config list
  update-ca-certificates  
fi

