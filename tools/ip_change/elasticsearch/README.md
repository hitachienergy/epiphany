# Changing IP for Elasticsearch infrastructure

## Requirements:

- Note all actual and desired ip configurations for Elasticsearch node
- User with sudo privileges

## Update configuration

1. Update /etc/hosts file

Execute `1_update_hosts.sh` script:

  ```bash
  sudo ./1_update_hosts.sh "CURRENT_IP" "NEW_IP"
  ```

  This script will update /etc/hosts file

2. Update Elasticsearch and Kibana configuration.

Execute `2_config_files.sh` script:

```bash
sudo ./2_config_files.sh "CURRENT_IP" "NEW_IP"
```

This script will update files:

--* /etc/elasticsearch/elasticsearch.yml
--* /etc/kibana/kibana.yml

Both services will be restarted.

3. Update Filebeat configuration on every host in cluster to setup new Elasticseach's ip.

 Execute `3_update_filebeat.sh` script on all cluster nodes.
 This will also restart filebeat service.

```bash
sudo ./3_update_filebeat.sh "CURRENT_IP" "NEW_IP"
```
