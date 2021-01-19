#/usr/bin/env sh

set -e

read -p "This script will stop and reconfigure kubelet/docker services, then reboot all k8s worker nodes. Are you sure (y/N)? " CHOICE
case "$CHOICE" in
  y|yes|Y|Yes) ;;
  *) exit ;;
esac

exec ansible-playbook -vv main.yml
