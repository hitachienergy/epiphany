#!/bin/bash -eu

yum-config-manager --disable epirepo
yum clean all --disablerepo='*' --enablerepo=epirepo
yum repolist