# How to upgrade from Ubuntu 18.04 to 20.04

Epiphany doesn't provide automation to perform Ubuntu release upgrade.

For information about upgrading Ubuntu release, please refer to [Ubuntu documentation](https://ubuntu.com/server/docs/upgrade-introduction).

For testing purposes, we use Ansible playbook ([ci/ansible/playbooks/os/ubuntu/upgrade-release.yml](../../../ci/ansible/playbooks/os/ubuntu/upgrade-release.yml)),
however it is strongly recommended that an administrator is involved to prepare for and perform the upgrade.

# How to upgrade from RHEL 7.x to RHEL 8.x

Epiphany doesn't provide automation to perform Red Hat Enterprise Linux release upgrade.

For information about upgrading RHEL release, please refer to [RHEL documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/upgrading_from_rhel_7_to_rhel_8/index).


For testing purposes, we use Ansible playbook ([ci/ansible/playbooks/os/rhel/upgrade-release.yml](../../../ci/ansible/playbooks/os/rhel/upgrade-release.yml)),
however it is strongly recommended that an administrator is involved to prepare for and perform the upgrade. This feature is still in experimental stage and is not fully operational yet.

# CentOS upgrade

Epiphany does not support upgrade of CentOS system since it's not supported in Epiphany 2.x at all. We switched to AlmaLinux 8 instead.
