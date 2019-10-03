#!/bin/bash -eu

yum-config-manager --disable epirepo
yum makecache
yum repolist
