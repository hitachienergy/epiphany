# Changing IP for Prometheus infrastructure

## Requirements:

- Note all actual and desired ip configurations for Prometheus node
- User with sudo privileges

## Update configuration

Prometheus configuration delivered by Epiphany uses hostnames in configuration files.
To apply ip change administrator needs to modify hosts inserts in /etc/hosts if IPs have changed.
You need to apply this change even if you changed only ip for Prometheus targets.

1. Update /etc/hosts file

Execute `1_update_hosts.sh` script:

  ```bash
  sudo ./1_update_hosts.sh "CURRENT_IP" "NEW_IP"
  ```

  This script will update /etc/hosts file. Script needs to be run on and for every node defined in /etc/hosts file

Example:

  ```bash
  sudo ./1_update_hosts.sh "CURRENT_IP" "NEW_IP"
  sudo ./1_update_hosts.sh "TARGET1_CURRENT_IP" "TARGET1_NEW_IP"
  ...
  sudo ./1_update_hosts.sh "TARGETx_CURRENT_IP" "TARGETx_NEW_IP"
  ```
