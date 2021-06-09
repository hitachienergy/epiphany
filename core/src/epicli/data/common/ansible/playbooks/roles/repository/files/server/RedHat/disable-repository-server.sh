#!/bin/bash -eu

if [[ -z $(which systemctl) ]]; then
  service httpd stop
  chkconfig httpd off
else
  systemctl stop httpd
  systemctl disable httpd
fi