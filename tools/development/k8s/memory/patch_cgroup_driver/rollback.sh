#/usr/bin/env sh

set -e

read -p "This script will stop and reconfigure kubelet/docker services, then reboot all k8s worker nodes. Are you sure (y/N)? " CHOICE
case "$CHOICE" in
  y|yes|Y|Yes) ;;
  *) exit ;;
esac

ansible-playbook -e old_cgroup_driver=systemd -e new_cgroup_driver=cgroupfs -vv main.yml
