#!/bin/bash

set -o errexit -o nounset -o pipefail

export AUTOSSH_PIDFILE=/tmp/autossh-kubectl-tunnel.pid

is_port_available() {
  local port=$1

  # nc command is much faster than lsof and doesn't require sudo to take into account ports used by other users
  nc -z 127.0.0.1 "$port" && return 1 || return 0 # 0 if port is available
}

if [ "$1" = "--kill" ]; then
  LOCAL_PORT=$2

  # kill autossh (ssh is child process)
  if test -f $AUTOSSH_PIDFILE; then
    echo "PID file found"
    AUTOSSH_PID=$(<$AUTOSSH_PIDFILE)
    echo "Processes to kill (PID $AUTOSSH_PID):"
    pstree -p "$AUTOSSH_PID"
    kill "$AUTOSSH_PID" # removes $AUTOSSH_PIDFILE
  fi

  # verify
  echo "Checking if local port ($LOCAL_PORT) is available"
  if is_port_available "$LOCAL_PORT"; then
    echo "OK"
  else
    echo "ERROR: Local port ($LOCAL_PORT) is in use" 1>&2
    exit 98
  fi
else # open tunnel
  LOCAL_PORT="$1"
  shift
  echo "autossh" "$@"
  autossh "$@"
  echo "Verifying"
  # wait for tunnel
  if timeout 20 sh -c "until nc -z 127.0.0.1 $LOCAL_PORT; do sleep 0.5; done"; then
    echo "OK"
  else
    RC=$?
    echo "ERROR: Connect timeout" 1>&2
    exit $RC
  fi
fi
