# Changing IP for Kafka infrastructure

## Requirements:

- Note all actual and desired ip configurations for Elasticsearch node
- User with sudo privileges

## Update configuration

Kafka and Zookeeper configuration delivered by Epiphany uses hostnames in configuration files.
To apply ip change administrator needs to modify hosts inserts in /etc/hosts configuration file.

1. Update /etc/hosts file

Execute `1_update_hosts.sh` script:

  ```bash
  sudo ./1_update_hosts.sh "CURRENT_IP" "NEW_IP"
  ```

  This script will update /etc/hosts file. Script needs to be run on and for every Kafka node.

Example:

  ```bash
  sudo ./1_update_hosts.sh "MASTER_CURRENT_IP" "MASTER_NEW_IP"
  sudo ./1_update_hosts.sh "SLAVE1_CURRENT_IP" "SLAVE1_NEW_IP"
  ...
  sudo ./1_update_hosts.sh "SLAVEx_CURRENT_IP" "SLAVEx_NEW_IP"
  ```
