## How to upgrade Kubernetes cluster

Upgrade procedure might be different for each Kubernetes version. Upgrade shall be done only from one minor version to next minor version. For example, upgrade from 1.9 to 1.11 looks like this:

```text
1.9.x -> 1.9.y
1.9.y -> 1.10
1.10  -> 1.11
```

Each version can be upgraded in a bit different way, to find information how to upgrade your version of Kubernetes please use this [guide](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/#kubeadm-upgrade-guidance).

Epiphany uses kubeadm to boostrap a cluster and the same tool is also used to upgrade it.

Upgrading Kubernetes cluster with running applications shall be done step by step. To prevent your applications downtime you should use at least **two Kubernetes worker nodes** and at least **two instances of each of your service**.

Start cluster upgrade with upgrading master node. Detailed instructions how to upgrade each node, including master, are described in guide linked above. When Kubernetes master is down it does not affect running applications, at this time only control plane is not operating. **Your services will be running but will not be recreated nor scaled when control plane is down.**

Once master upgrade finished successfully, you shall start upgrading nodes - **one by one**. Kubernetes master will notice when worker node is down and it will instatiate services on existing operating node, that is why it is essential to have more than one worker node in cluster to minimize applications downtime.

## How to upgrade Kubernetes cluster from 1.13.0 to 1.13.1

Detailed instruction can be found in [Kubernetes upgrade to 1.13 documentation](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade-1-13/)

### Ubuntu Server

#### Upgrade Master

```bash
# RUN ON MASTER

1. sudo kubeadm version # should show v1.13.0
2. sudo kubeadm upgrade plan v1.13.1

3. apt update
4. apt-cache policy kubeadm


5. sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm=1.13.1-00 && \
sudo apt-mark hold kubeadm

6. sudo kubeadm version # should show v1.13.1
7. sudo kubeadm upgrade plan v1.13.1

8. sudo kubeadm upgrade apply v1.13.1

9. sudo apt-mark unhold kubelet && \
sudo apt-get update && sudo apt-get install -y kubelet=1.13.1-00 && \
sudo apt-mark hold kubelet
```

#### Upgrade Worker Nodes

Commands below should be run in context of each node in the cluster. Variable `$NODE` represents node name (node names can be retrieved by command `kubectl get nodes` on master)

Worker nodes will be upgraded one by one - it will prevent application downtime.

```bash

# RUN ON WORKER NODE - $NODE

1. sudo apt-mark unhold kubectl && \
sudo apt-get update && sudo apt-get install -y kubectl=1.13.1-00 && \
sudo apt-mark hold kubectl

# RUN ON MASTER

2. kubectl drain $NODE --ignore-daemonsets

# RUN ON WORKER NODE - $NODE

3. sudo kubeadm upgrade node config --kubelet-version v1.13.1

4. sudo apt-get update
5. sudo apt-get install -y kubelet=1.13.1-00 kubeadm=1.13.1-00

6. sudo systemctl restart kubelet
7. sudo systemctl status kubelet # should be running

# RUN ON MASTER

8. kubectl uncordon $NODE

9. # go to 1. for next node

# RUN ON MASTER
10. kubectl get nodes # should return nodes in status "Ready" and version 1.13.1

```

### RHEL

#### Upgrade Docker version

Upgrading Kubernetes to 1.13.1 on RHEL requires Docker upgrade. Newer Docker packages exist in docker-ce repository but you can use newer Docker-ee if you need. Verified Docker versions for Kubernetes are: 1.11.1, 1.12.1, 1.13.1, 17.03, 17.06, 17.09, 18.06. [Go to K8s docs](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.13.md#external-dependencies)

```bash

# Remove previous docker version
1 sudo yum remove docker \
                  docker-common \
                  container-selinux \
                  docker-selinux \
                  docker-engine
2. sudo rm -rf /var/lib/docker
3. sudo rm -rf /run/docker
4. sudo rm -rf /var/run/docker
5. sudo rm -rf /etc/docker

# Add docker-ce repository
6. sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
7. sudo yum makecache fast
8. sudo yum -y install docker-ce-18.06.3.ce-3.el7

```

#### Upgrade Master

```bash
# RUN ON MASTER

1. sudo kubeadm version # should show v1.13.0
2. sudo kubeadm upgrade plan v1.13.1

3. sudo yum install -y kubeadm-1.13.1-0 --disableexcludes=kubernetes

4. sudo kubeadm version # should show v1.13.1
5. sudo kubeadm upgrade plan v1.13.1

6. sudo kubeadm upgrade apply v1.13.1

7. sudo yum install -y kubelet-1.13.1-0 --disableexcludes=kubernetes

```

#### Upgrade Worker Nodes

Commands below should be run in context of each node in the cluster. Variable `$NODE` represents node name (node names can be retrieved by command `kubectl get nodes` on master)

Worker nodes will be upgraded one by one - it will prevent application downtime.

```bash

# RUN ON WORKER NODE - $NODE

1. yum install -y kubectl-1.13.1-0 --disableexcludes=kubernetes

# RUN ON MASTER

2. kubectl drain $NODE --ignore-daemonsets

# RUN ON WORKER NODE - $NODE

3. # Upgrade Docker version using instruction from above

4. sudo kubeadm upgrade node config --kubelet-version v1.13.1

5. sudo yum install -y kubelet-1.13.1-0 kubeadm-1.13.1-0 --disableexcludes=kubernetes

6. sudo systemctl restart kubelet
7. sudo systemctl status kubelet # should be running

# RUN ON MASTER

8. kubectl uncordon $NODE

9. # go to 1. for next node

# RUN ON MASTER
10. kubectl get nodes # should return nodes in status "Ready" and version 1.13.1

```

## How to upgrade Kubernetes cluster from 1.13.1 to 1.13.10 / latest patch

### Ubuntu Server

#### Upgrade Master

Variable `$MASTER` represents master node name (node names can be retrieved by command `kubectl get nodes` on master)

##### > RUN ON MASTER

1. Check kubeadm version
```bash
kubeadm version
# should show v1.13.1
```
2. Find the latest stable 1.13 version
```bash
sudo apt update
apt-cache policy kubeadm 
# 1.13.10-0
```
3. Drain master in preparation for maintenance
```bash
kubectl drain $MASTER # [--ignore-daemonsets] [--delete-local-data]
# $MASTER should be marked as Ready,SchedulingDisabled
```
may need to use flags:
```bash
--ignore-daemonsets: # to ignore DaemonSet-managed pods

--delete-local-data: # to continue even if there are pods using emptyDir (local data that will be deleted when the node is drained)
# BE CAREFUL!
```
4. Wait for all pods to be running and ready

5. Install packages
```bash
sudo apt-mark unhold kubernetes-cni kubelet kubectl kubeadm && \
sudo apt-get update && sudo apt-get install kubernetes-cni=0.7.5-00 kubelet=1.13.10-00 kubectl=1.13.10-00 kubeadm=1.13.10-00 && \
sudo apt-mark hold kubernetes-cni kubelet kubectl kubeadm
```
6. Validate whether current cluster is upgradeable 
```bash
sudo kubeadm upgrade plan v1.13.10 # [--config /path/to/kubeadm-config.yml]
```
7. Upgrade Kubernetes cluster to the specified version
```bash
sudo kubeadm upgrade apply v1.13.10 # [--config /path/to/kubeadm-config.yml]
```
8. Wait for all pods to be running and ready

9. Reload daemon
```bash
sudo systemctl daemon-reload
```
10. Restart kubelet
```bash
sudo systemctl restart kubelet
```
11. Check kubelet status
```bash
sudo systemctl status kubelet
# should be active (running)
```
12. Wait for cluster to be ready, e.g. check:
```bash
kubectl cluster-info
```
13. Uncordon master - mark as schedulable
```bash
kubectl uncordon $MASTER
```
14. List all nodes
```bash
kubectl get nodes
# should return $MASTER in status "Ready" and version 1.13.10
```

#### Upgrade Worker Nodes

Commands below should be run in context of each node in the cluster. Variable `$NODE` represents node name (node names can be retrieved by command `kubectl get nodes` on master)

Important: Worker nodes should be upgraded one by one - this will prevent application downtime.

##### > RUN ON MASTER

1. Drain node in preparation for maintenance
```bash
kubectl drain $NODE # [--ignore-daemonsets] [--delete-local-data]
# $NODE should be marked as Ready,SchedulingDisabled
```
may need to use flags:
```bash
--ignore-daemonsets: # to ignore DaemonSet-managed pods

--delete-local-data: # to continue even if there are pods using emptyDir (local data that will be deleted when the node is drained)
# BE CAREFUL!
```
2. Wait for all pods to be running and ready

##### > RUN ON NODE

3. Install packages
```bash
sudo apt-mark unhold kubernetes-cni kubelet kubectl kubeadm && \
sudo apt-get update && sudo apt-get install kubernetes-cni=0.7.5-00 kubelet=1.13.10-00 kubectl=1.13.10-00 kubeadm=1.13.10-00 && \
sudo apt-mark hold kubernetes-cni kubelet kubectl kubeadm
```
4. Upgrade node config
```bash
sudo kubeadm upgrade node config --kubelet-version v1.13.10
```
5. Reload daemon
```bash
sudo systemctl daemon-reload
```
6. Restart kubelet
```bash
sudo systemctl restart kubelet
```
7. Check kubelet status
```bash
sudo systemctl status kubelet
# should be active (running)
```
##### > RUN ON MASTER

8. Uncordon node - mark as schedulable
```bash
kubectl uncordon $NODE
```
9. List all nodes
```bash
kubectl get nodes
# should return $NODE in status "Ready" and version 1.13.10
```
10. Go back to the point 1 with the next node


### RHEL

#### Upgrade Master

Variable `$MASTER` represents master node name (node names can be retrieved by command `kubectl get nodes` on master)

##### > RUN ON MASTER

1. Check kubeadm version
```bash
kubeadm version
# should show v1.13.1
```
2. Find the latest stable 1.13 version
```bash
yum list --showduplicates kubeadm --disableexcludes=kubernetes 
# 1.13.10-0
```
3. Drain master in preparation for maintenance
```bash
kubectl drain $MASTER # [--ignore-daemonsets] [--delete-local-data]
# $MASTER should be marked as Ready,SchedulingDisabled
```
may need to use flags:
```bash
--ignore-daemonsets: # to ignore DaemonSet-managed pods

--delete-local-data: # to continue even if there are pods using emptyDir (local data that will be deleted when the node is drained)
# BE CAREFUL!
```
4. Wait for all pods to be running and ready

5. Install packages
```bash
sudo yum install kubernetes-cni-0.7.5-0 kubelet-1.13.10-0 kubectl-1.13.10-0 kubeadm-1.13.10-0 --disableexcludes=kubernetes
```
6. Validate whether current cluster is upgradeable 
```bash
sudo kubeadm upgrade plan v1.13.10 # [--config /path/to/kubeadm-config.yml]
```
7. Upgrade Kubernetes cluster to the specified version
```bash
sudo kubeadm upgrade apply v1.13.10 # [--config /path/to/kubeadm-config.yml]
```
8. Wait for all pods to be running and ready

9. Reload daemon
```bash
sudo systemctl daemon-reload
```
10. Restart kubelet
```bash
sudo systemctl restart kubelet
```
11. Check kubelet status
```bash
sudo systemctl status kubelet
# should be active (running)
```
12. Wait for cluster to be ready, e.g. check:
```bash
kubectl cluster-info
```
13. Uncordon master - mark as schedulable
```bash
kubectl uncordon $MASTER
```
14. List all nodes
```bash
kubectl get nodes
# should return $MASTER in status "Ready" and version 1.13.10
```

#### Upgrade Worker Nodes

Commands below should be run in context of each node in the cluster. Variable `$NODE` represents node name (node names can be retrieved by command `kubectl get nodes` on master)

Important: Worker nodes should be upgraded one by one - this will prevent application downtime.

##### > RUN ON MASTER

1. Drain node in preparation for maintenance
```bash
kubectl drain $NODE # [--ignore-daemonsets] [--delete-local-data]
# $NODE should be marked as Ready,SchedulingDisabled
```
may need to use flags:
```bash
--ignore-daemonsets: # to ignore DaemonSet-managed pods

--delete-local-data: # to continue even if there are pods using emptyDir (local data that will be deleted when the node is drained)
# BE CAREFUL!
```
2. Wait for all pods to be running and ready

##### > RUN ON NODE

3. Install packages
```bash
sudo yum install kubernetes-cni-0.7.5-0 kubelet-1.13.10-0 kubectl-1.13.10-0 kubeadm-1.13.10-0 --disableexcludes=kubernetes
```
4. Upgrade node config
```bash
sudo kubeadm upgrade node config --kubelet-version v1.13.10
```
5. Reload daemon
```bash
sudo systemctl daemon-reload
```
6. Restart kubelet
```bash
sudo systemctl restart kubelet
```
7. Check kubelet status
```bash
sudo systemctl status kubelet
# should be active (running)
```
##### > RUN ON MASTER

8. Uncordon node - mark as schedulable
```bash
kubectl uncordon $NODE
```
9. List all nodes
```bash
kubectl get nodes
# should return $NODE in status "Ready" and version 1.13.10
```
10. Go back to the point 1 with the next node

## How to upgrade Kafka cluster

### Kafka upgrade

No downtime upgrades are possible to achieve when upgrading Kafka, but before you start thinking about upgrading you have to think about your topics configuration. Kafka topics are distributed accross partitions with replication. Default value for replication is 3, it means each partition will be replicated to 3 brokers. You should remember to enable redundancy and keep **at least two replicas all the time**, it is important when upgrading Kafka cluser. When one of your Kafka nodes will be down during upgrade ZooKeeper will direct your producers and consumers to working instances - having replicated partitions on working nodes will ensure no downtime and no data loss work.

Upgrading Kafka could be different for every Kafka release, please refer to [Apache Kafka documentation](https://kafka.apache.org/documentation/#upgrade). Important point to remember during Kafka upgrade is the rule: **only one broker at the time** - to prevent downtime you should uprage you Kafka brokers one by one.

### ZooKeeper upgrade

ZooKeeper redundancy is also recommended, since service restart is required during upgrade - it can cause ZooKeeper unavailability. Having at **least two ZooKeeper services** in *ZooKeepers ensemble* you can upgrade one and then start with the rest **one by one**.

More detailed information about ZooKeeper you can find in  [ZooKeeper documentation](https://cwiki.apache.org/confluence/display/ZOOKEEPER).