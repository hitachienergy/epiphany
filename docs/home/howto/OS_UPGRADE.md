# How to upgrade from Ubuntu 18.04 to 20.04

Epiphany doesn't provide automation to perform Ubuntu release upgrade.

For information about upgrading Ubuntu release, please refer to [Ubuntu documentation](https://ubuntu.com/server/docs/upgrade-introduction).

For testing purposes, we use Ansible playbook ([ci/ansible/playbooks/os/ubuntu/upgrade-release.yml](../../../ci/ansible/playbooks/os/ubuntu/upgrade-release.yml)),
however it is strongly recommended that an administrator is involved to prepare for and perform the upgrade.
