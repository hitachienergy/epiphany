#!/bin/bash -eu

yum-config-manager --disable epirepo
yum clean all --enablerepo=epirepo --disablerepo='*'
yum repolist