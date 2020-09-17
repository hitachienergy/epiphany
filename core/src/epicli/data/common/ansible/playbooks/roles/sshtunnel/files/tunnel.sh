#!/bin/bash

set -o errexit

if [ "$1" = "--kill" ]; then
  ps -C ssh,autossh -o pid,cmd |
  grep -E "@${2}($|[[:blank:]])" |
  awk '{print $1}' |
  xargs -r kill
else
  autossh "$@"
fi