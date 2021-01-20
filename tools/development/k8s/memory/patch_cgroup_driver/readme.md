[K8s documentation](https://kubernetes.io/docs/setup/production-environment/container-runtimes/#cgroup-drivers) states:

> A single cgroup manager simplifies the view of what resources are being allocated and will by default have a more consistent view of the available and in-use resources.
> When there are two cgroup managers on a system, you end up with two views of those resources.
> In the field, people have reported cases where nodes that are configured to use cgroupfs for the kubelet and Docker, but systemd for the rest of the processes, become unstable under resource pressure.

Unfortunately (before this workaround) Epiphany had never switched to the `systemd` cgroup driver for `docker` and `kubelet` services.
Our aim here is to take an existing Epiphany cluster, patch worker nodes and perform memory and cpu stress tests on it.

## Requirements

- an existing Epiphany cluster with Kubernetes deployed
- a valid inventory file
- a valid private key (to connect to VMs)
- `ansible-playbook` command installed
- `sh` command installed

## Usage

1. Copy your cluster's `inventory` file to this directory.

2. Run `sh apply.sh`.

## Procedure

Ansible will sequentially (rolling update but **without waiting for pods to be `Ready`**) reconfigure `docker` and `kubelet` services on each worker node.

When there are any changes found in config files, ansible will (for each worker node):

1. Drain all user-deployed pods.

2. Stop docker and kubelet services.

3. Reconfigure docker and kubelet services to use `systemd` cgroup driver.

4. Reboot.

5. Uncordon (re-enable pod scheduling).

6. Make sure operations are idempotent.
