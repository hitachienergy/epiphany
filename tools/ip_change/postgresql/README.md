# Changing IP for Database infrastructure

## Requirements:

- Note all actual and desired ip configurations for master and all slaves (if exist)
- User with sudo privileges

## Note that host ip change may impact database when data contains any network address types

See more: <https://www.postgresql.org/docs/10/datatype-net-types.html>

## Master Node

This part describes actions to execute on Master Database Node

1. Execute `1_update_hosts.sh` script to update `/etc/hosts file`.

  ```bash
  sudo ./1_update_hosts.sh "CURRENT_IP" "NEW_IP"
  ```
   This part needs to be run once per every database (Master and Slave) record in `/etc/hosts` file:
  ```bash
  sudo ./1_update_hosts.sh "MASTER_CURRENT_IP" "MASTER_NEW_IP"
  sudo ./1_update_hosts.sh "SLAVE1_CURRENT_IP" "SLAVE1_NEW_IP"
  ...
  sudo ./1_update_hosts.sh "SLAVEx_CURRENT_IP" "SLAVEx_NEW_IP"
  ```

2. This steps need to be executed only for Master-Slave(s) configuration:

  Update host-based authentication file:
  ```bash
  sudo ./2_update_pg_hba.sh "SLAVE1_CURRENT_IP" "SLAVE1_NEW_IP"
  sudo ./2_update_pg_hba.sh "SLAVE2_CURRENT_IP" "SLAVE2_NEW_IP"
  ...
  sudo ./2_update_pg_hba.sh "SLAVEx_CURRENT_IP" "SLAVEx_NEW_IP"
  ```

  This command needs to run for every Slave's record in pg_hba.conf file

## Slave Node(s)

This part describes actions to execute on Slave Database Nodes

1. Execute `1_update_hosts.sh` script to update `/etc/hosts file`.

  ```bash
  sudo ./1_update_hosts.sh "CURRENT_IP" "NEW_IP"
  ```
   This part needs to be run once per every database (Master and Slave) record in `/etc/hosts` file:
  ```bash
  sudo ./1_update_hosts.sh "MASTER_CURRENT_IP" "MASTER_NEW_IP"
  sudo ./1_update_hosts.sh "SLAVE1_CURRENT_IP" "SLAVE1_NEW_IP"
  ...
  sudo ./1_update_hosts.sh "SLAVEx_CURRENT_IP" "SLAVEx_NEW_IP"
  ```

2. Execute `3_update_pgpass.sh` on every Slave Node
```bash
sudo ./3_update_pgpass.sh "MASTER_CURRENT_IP" "MASTER_NEW_IP"
```
This script will update connection string to Master Database

3. Update any other application connection strings to establish connection to new address.
