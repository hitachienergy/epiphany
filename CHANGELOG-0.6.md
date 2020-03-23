# Changelog 0.6

## [0.6.0] 2020-03-xx

### Added

- [#986](https://github.com/epiphany-platform/epiphany/issues/986) - Add vim to Epicli container and devcontainer
- [#987](https://github.com/epiphany-platform/epiphany/issues/987) - Add verbosity levels for Terraform and Ansible
- [#656](https://github.com/epiphany-platform/epiphany/issues/656) - Add logrotation to kafka by size
- [#1016](https://github.com/epiphany-platform/epiphany/issues/1016) - Disable verify , backup and recovery as they are not fully implemented
- [#1044](https://github.com/epiphany-platform/epiphany/issues/1044) - Add ability to add subscriptionId to sp.yml on Azure

### Fixed

- [#624](https://github.com/epiphany-platform/epiphany/issues/624) - Don't run epicli as root in container
- [#966](https://github.com/epiphany-platform/epiphany/issues/966) - Ubuntu builds get stuck on 'Create epirepo repository' task waiting for user input in offline mode
- [#1043](https://github.com/epiphany-platform/epiphany/issues/1043) - For vm template on Azure disk_size_gb is missing in storage_os_disk
