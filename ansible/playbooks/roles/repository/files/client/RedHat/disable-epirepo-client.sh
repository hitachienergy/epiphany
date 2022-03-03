#!/bin/bash -eu

dnf config-manager --set-disabled epirepo
dnf clean all --disablerepo='*' --enablerepo=epirepo
dnf repolist
