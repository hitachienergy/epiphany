#!/bin/bash

set -o errexit -o nounset -o pipefail

export AUTOSSH_PIDFILE=/tmp/autossh-kubectl-tunnel.pid

if [ "$1" = "--kill" ]; then
  LOCAL_PORT="$2"

  if test -f $AUTOSSH_PIDFILE; then
    echo "PID file found"
    AUTOSSH_PID=$(<$AUTOSSH_PIDFILE)
    echo "Processes to kill (PID $AUTOSSH_PID):"
    pstree -p "$AUTOSSH_PID"
    kill "$AUTOSSH_PID" # removes $AUTOSSH_PIDFILE
  fi

  echo "Checking if local port ($LOCAL_PORT) is free"
  if lsof -i:"$LOCAL_PORT"; then
    echo "ERROR: Local port ($LOCAL_PORT) still in use"
    exit 98
  else
    echo "OK"
  fi
else # open tunnel
  LOCAL_PORT="$1"
  shift
  echo "autossh $@"
  autossh "$@"
  # verify (fails if port is not in use)
  lsof -i:"$LOCAL_PORT"
fi
