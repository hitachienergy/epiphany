# Changing IP for configured Kubernetes claster.

## WARNING: Cluster downtime will be required.
## WARNING: Solution was validated for Kubernetes version 1.14.x.

### I. Kubernetes Master IP change procedure:

1. Note current Kubernetes Master IP
2. Note new Kubernetes Master IP (do not change machine IP yet)
3. Execute `start.sh` script with replacing placeholder strings respectively.
```bash
./start.sh "CURRENT_MASTER_IP" "NEW_MASTER_IP"
```

4. If all actions completed successfully change IP address of Master machine.
5. Execute once again `start.sh` with additional parameter.
```bash
./start.sh "CURRENT_MASTER_IP" "NEW_MASTER_IP" "1"
```
6. Note join credentials printed in last step `token`, `cert hash`, `server api url` values. Those will be used to join worker Nodes in next step. Credentials are valid only for 4 hours.

### For each Kubernetes worker Node

1. On each Kubernetes worker Node update /etc/hosts with new IP or using following command:
```bash
./3_update_hosts.sh "CURRENT_MASTER_IP" "NEW_MASTER_IP"
```
2. Modify `/etc/kubeadm/kubeadm-join.yml` file using values from `I.6.`

3. Execute command to reset worker Node.
```bash
sudo kubeadm reset
```
3. Execute command to join node back to the cluster:
```bash
sudo kubeadm join --config=/etc/kubeadm/kubeadm-join.yml
```
