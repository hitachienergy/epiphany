## Replication / configuration

Configuration data is stored in location: /var/lib/ceph
Storage data is located on dedicated devices which are connected via OSD pods.

Replication: Like Ceph Clients, Ceph OSD Daemons use the CRUSH algorithm, but the Ceph OSD Daemon uses it to compute where replicas of objects should be stored (and for rebalancing). In a typical write scenario, a client uses the CRUSH algorithm to compute where to store an object, maps the object to a pool and placement group, then looks at the CRUSH map to identify the primary OSD for the placement group.
The client writes the object to the identified placement group in the primary OSD. Then, the primary OSD with its own copy of the CRUSH map identifies the secondary and tertiary OSDs for replication purposes, and replicates the object to the appropriate placement groups in the secondary and tertiary OSDs (as many OSDs as additional replicas), and responds to the client once it has confirmed the object was stored successfully.

## Prerequisite


Since version 1.4 lvm package present on the nodes is required. It applies for AWS machines (not tested on Ubuntu)
Example installation command:

RHEL:

`yum install lvm2 -y`

## Rook ceph design

https://rook.io/docs/rook/v1.4/ceph-storage.html

## Cluster setup

Rook ceph cluster can be easily deployed using example default definitions from GH repo:

`git clone --single-branch --branch release-1.4 https://github.com/rook/rook.git`

open location:

`rook/cluster/examples/kubernetes/ceph`

and list examples:
```
    -rw-r--r--. 1 root root 395 Jul 28 13:00 ceph-client.yaml
    -rw-r--r--. 1 root root 1061 Jul 28 13:00 cluster-external-management.yaml
    -rw-r--r--. 1 root root 886 Jul 28 13:00 cluster-external.yaml
    -rw-r--r--. 1 root root 5300 Jul 28 13:00 cluster-on-pvc.yaml
    -rw-r--r--. 1 root root 1144 Jul 28 13:00 cluster-test.yaml
    -rw-r--r--. 1 root root 10222 Jul 28 14:47 cluster.yaml
    -rw-r--r--. 1 root root 2143 Jul 28 13:00 common-external.yaml
    -rw-r--r--. 1 root root 44855 Jul 28 13:00 common.yaml
    -rw-r--r--. 1 root root 31424 Jul 28 13:00 create-external-cluster-resources.py
    -rw-r--r--. 1 root root 2641 Jul 28 13:00 create-external-cluster-resources.sh
    drwxr-xr-x. 5 root root 47 Jul 28 13:00 csi
    -rw-r--r--. 1 root root 363 Jul 28 13:00 dashboard-external-https.yaml
    -rw-r--r--. 1 root root 362 Jul 28 13:00 dashboard-external-http.yaml
    -rw-r--r--. 1 root root 839 Jul 28 13:00 dashboard-ingress-https.yaml
    -rw-r--r--. 1 root root 365 Jul 28 13:00 dashboard-loadbalancer.yaml
    -rw-r--r--. 1 root root 1554 Jul 28 13:00 direct-mount.yaml
    -rw-r--r--. 1 root root 3308 Jul 28 13:00 filesystem-ec.yaml
    -rw-r--r--. 1 root root 780 Jul 28 13:00 filesystem-test.yaml
    -rw-r--r--. 1 root root 4286 Jul 28 13:00 filesystem.yaml
    drwxr-xr-x. 2 root root 115 Jul 28 13:00 flex
    -rw-r--r--. 1 root root 4530 Jul 28 13:00 import-external-cluster.sh
    drwxr-xr-x. 2 root root 183 Jul 28 13:00 monitoring
    -rw-r--r--. 1 root root 1409 Jul 28 13:00 nfs.yaml
    -rw-r--r--. 1 root root 495 Jul 28 13:00 object-bucket-claim-delete.yaml
    -rw-r--r--. 1 root root 495 Jul 28 13:00 object-bucket-claim-retain.yaml
    -rw-r--r--. 1 root root 2306 Jul 28 13:00 object-ec.yaml
    -rw-r--r--. 1 root root 2313 Jul 28 13:00 object-openshift.yaml
    -rw-r--r--. 1 root root 698 Jul 28 13:00 object-test.yaml
    -rw-r--r--. 1 root root 488 Jul 28 13:00 object-user.yaml
    -rw-r--r--. 1 root root 3573 Jul 28 13:00 object.yaml
    -rw-r--r--. 1 root root 19075 Jul 28 13:00 operator-openshift.yaml
    -rw-r--r--. 1 root root 18199 Jul 28 13:00 operator.yaml
    -rw-r--r--. 1 root root 1080 Jul 28 13:00 pool-ec.yaml
    -rw-r--r--. 1 root root 508 Jul 28 13:00 pool-test.yaml
    -rw-r--r--. 1 root root 1966 Jul 28 13:00 pool.yaml
    -rw-r--r--. 1 root root 410 Jul 28 13:00 rgw-external.yaml
    -rw-r--r--. 1 root root 2273 Jul 28 13:00 scc.yaml
    -rw-r--r--. 1 root root 682 Jul 28 13:00 storageclass-bucket-delete.yaml
    -rw-r--r--. 1 root root 810 Jul 28 13:00 storageclass-bucket-retain-external.yaml
    -rw-r--r--. 1 root root 681 Jul 28 13:00 storageclass-bucket-retain.yaml
    -rw-r--r--. 1 root root 1251 Jul 28 13:00 toolbox.yaml
    -rw-r--r--. 1 root root 6089 Jul 28 13:00 upgrade-from-v1.2-apply.yaml
    -rw-r--r--. 1 root root 14957 Jul 28 13:00 upgrade-from-v1.2-crds.yaml
```

After creating basic setup (`common.yaml`, `operator.yaml`, `cluster.yaml`) install toolbox (`toolbox.yaml`) as well for checking the ceph cluster status.

**IMPORTANT**:

ensure the **osd** container is created and running. It requires a storage device to be available on the nodes.

During cluster startup it searches for the devices available and creates osd containers for them.

Kubelet nodes have to use a default flag `enable-controller-attach-detach` set to `true`. Otherwise PVC will not attach to the pod.

Location of the file where we can find the flag:

```
/var/lib/kubelet/kubeadm-flags.env 
```

on every worker nodes with kubelet. After that we need to restart kubelet: 
```
systemctl restart kubelet
```

If cluster is working we can create a storage which can be one of a type:

```
Block: Create block storage to be consumed by a pod
```
```
Object: Create an object store that is accessible inside or outside the 
Kubernetes cluster
```
```
Shared Filesystem: Create a filesystem to be shared across multiple pods
```

Eg. 

  -> `filesystem.yaml` and then

  -> `storageclass.yaml`

CRD:

There are 2 ways cluster can be set up:

- Host-based Cluster
- PVC-based Cluster

PVC example:

```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: rbd-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: rook-ceph-block
```

Application using PVC example:

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql
  namespace: default
  labels:
    k8s-app: postgresql
    kubernetes.io/cluster-service: "true"
spec:
  replicas: 1
  selector:
    matchLabels:
      k8s-app: postgresql
  template:
    metadata:
      labels:
        k8s-app: postgresql
        kubernetes.io/cluster-service: "true"
    spec:
      containers:
        - name: postgres
          image: postgres:10.1
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: dbdb
            - name: POSTGRES_USER
              value: test
            - name: POSTGRES_PASSWORD
              value: test
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          volumeMounts:
            - mountPath: "/var/lib/postgresql/data"
              name: "image-store"
      volumes:
      - name: image-store
        persistentVolumeClaim:
          claimName: rbd-pvc
          readOnly: false
```


Choosing Block Storage which allows a single pod to mount storage, be aware that if one node where Your application is hosted will crash, all the pods located on the crashed node will go into terminating state and application will be unavailable since terminating pods blocking access to ReadWriteOnce volume and new pod can't create. You have to manually delete volume attachment or use CephFS instead of RBD.

Related discussion: https://stackoverflow.com/questions/61186199/why-does-kubernetes-not-terminating-pods-after-a-node-crash


## Internal k8s automated setup and tests 

Step by step procedure for setting environment up and testing it (together with backup/restore) is available in the following repo:
https://github.com/mkyc/k8s-rook-ceph

## Useful links:

Good starting point:

https://rook.io/docs/rook/v1.4/ceph-quickstart.html

Toolbox for debugging:

https://rook.io/docs/rook/v1.4/ceph-toolbox.html

Filesystem storage:

https://rook.io/docs/rook/v1.4/ceph-filesystem.html

Custom Resource Definitions:

https://rook.io/docs/rook/v1.4/ceph-cluster-crd.html

Add/remove osd nodes:
https://access.redhat.com/documentation/en-us/red_hat_ceph_storage/2/html/administration_guide/adding_and_removing_osd_nodes

Useful rook ceph guide:
https://www.cloudops.com/2019/05/the-ultimate-rook-and-ceph-survival-guide/
