# Changing IP for Elasticsearch infrastructure

## Requirements:

- Note all actual and desired ip configurations for Elasticsearch nodes
- User with sudo privileges

## Update configuration

1. Execute `1_update_hosts.sh` script. This script will update /etc/hosts file

  ```bash
  sudo ./1_update_hosts.sh "CURRENT_IP" "NEW_IP"
  ```

  This script will update /etc/hosts file

2. Execute `2_config_files.sh` script. This script will update files:

--* /etc/elasticsearch/elasticsearch.yml
--* /etc/kibana/kibana.yml

```bash
sudo ./2_config_files.sh "CURRENT_IP" "NEW_IP"
```

This script will update Elasticsearch and Kibana configuration files
and restart both applications
