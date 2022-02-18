# Kubernetes Persistent Storage

In Epiphany there are two supported ways of setting up Kubernetes Persistent Storage:
- Rook/Ceph Cluster Storage with disks resources created by Epiphany
- [Azure Files](https://docs.microsoft.com/en-us/azure/storage/files/storage-files-introduction)
or [Amazon EFS](https://docs.aws.amazon.com/efs/latest/ug/how-it-works.html) storage types to use as Kubernetes persistent volumes

## Kubernetes Rook/Ceph Cluster Storage

Rook provides distributed storage systems for Kubernetes installed with Epiphany.
It provides capabilities:
- self-managing
- self-scaling
- self-healing
- upgrading
- migration
- disaster recovery
- monitoring

Epiphany supports Rook with Ceph storage, other options provided by Rook - Cassandra, NFS are not supported.

In Epiphany Rook/Ceph is installed with using Helm Chart and may be configured according to needs with overriding default Helm Chart values with adding them to proper sections in Epiphany `configuration/rook`.

More information about Helm Chart values may be found:
- [Helm Operator](https://github.com/rook/rook/blob/master/Documentation/helm-operator.md)
- [Helm Ceph Cluster](https://github.com/rook/rook/blob/master/Documentation/helm-ceph-cluster.md)

Sample configuration files that can be used in Epiphany `configuration/rook`:
- [Helm Operator](https://raw.githubusercontent.com/rook/rook/v1.8.5/deploy/charts/rook-ceph/values.yaml)
- [Helm Ceph Cluster](https://raw.githubusercontent.com/rook/rook/v1.8.5/deploy/charts/rook-ceph-cluster/values.yaml)

More informations about Rook with Ceph storage may be found in the official Rook [documentation](https://rook.io/docs/rook/v1.8/).

### Rook/Ceph Cluster Storage - Azure

To create Rook/Ceph Cluster Storage first you need to add empty disk resource to Kubernetes cluster created by Epiphany.

### Rook/Ceph Cluster Storage - AWS

### Rook/Ceph Cluster Storage - On Prem

### Azure

#### Infrastructure

Epiphany creates a [storage account](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-overview)
with "Standard" tier and locally-redundant storage ("LRS" redundancy option). This storage account contains a file share
with the name "k8s".

With the following configuration it is possible to specify storage account name and "k8s" file
share [quota](https://docs.microsoft.com/en-us/azure/storage/files/storage-how-to-create-file-share) in GiB.

```yaml
---
kind: infrastructure/storage-share
name: default
provider: azure
specification:
  quota: 50
```

#### Kubernetes

There are a few related K8s objects created such as PersistentVolume, PersistentVolumeClaim and "azure-secret" Secret
when `specification.storage.enable` is set to `true`. It is possible to control pv/pvc names and storage
capacity/request in GiB with the configuration below.

---
**NOTE**

It makes no sense to specify greater capacity than Azure file share allows using. In general these values should be the
same.

---

```yaml
---
kind: configuration/kubernetes-master
name: default
provider: azure
specification:
  storage:
    name: epiphany-cluster-volume
    enable: true
    capacity: 50
```

#### Additional configuration

It is possible to use Azure file shares created by your own.
Check [documentation](https://docs.microsoft.com/en-us/azure/storage/files/storage-how-to-create-file-share) for
details. Created file shares may be used
in [different ways](https://github.com/kubernetes/examples/blob/master/staging/volumes/azure_file/README.md#pod-creation).
There are appropriate configuration examples below.

---
**NOTE**

Before applying configuration, storage access
[secret](https://github.com/kubernetes/examples/blob/master/staging/volumes/azure_file/README.md#create-a-storage-access-secret)
should be created

---

##### Direct approach

As Epiphany always creates a file share when `provider: azure` is used, in this case similar configuration can be used 
even with `specification.storage.enable` set to `false`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: azure1
spec:
  containers:
    - image: busybox
      name: azure
      command: [ "/bin/sh", "-c", "--" ]
      args: [ "while true; do sleep 30; done;" ]
      volumeMounts:
        - name: azure
          mountPath: /mnt/azure
  volumes:
    - name: azure
      azureFile:
        secretName: azure-secret
        shareName: k8s
        readOnly: false
```

##### Using persistent volumes

```yaml
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: epiphany-cluster-volume
spec:
  storageClassName: azurefile
  capacity:
    storage: 50Gi
    accessModes:
      - "ReadWriteMany"
  azureFile:
    secretName: azure-secret
    shareName: k8s
    readOnly: false
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
    name: epiphany-cluster-volume-claim
spec:
  storageClassName: azurefile
  volumeName: epiphany-cluster-volume
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 50Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: azure2
spec:
  containers:
    - image: busybox
      name: azure
      command: [ "/bin/sh", "-c", "--" ]
      args: [ "while true; do sleep 30; done;" ]
      volumeMounts:
        - name: azure
          mountPath: /mnt/azure
  volumes:
    - name: azure
      persistentVolumeClaim:
        claimName: epiphany-cluster-volume-claim
```

### AWS

#### Infrastructure

Amazon EFS can be configured using following configuration.

```yaml
---
kind: infrastructure/efs-storage
provider: aws
name: default
specification:
  encrypted: true
  performance_mode: generalPurpose
  throughput_mode: bursting
  #provisioned_throughput_in_mibps:  # The throughput, measured in MiB/s, that you want to provision for the file system. Only applicable when throughput_mode set to provisioned
```

#### Kubernetes

Configuration for AWS supports additional parameter `specification.storage.path` that allows specifying the path on EFS
to be accessed by pods. When `specification.storage.enable` is set to `true`, PersistentVolume and PersistentVolumeClaim
are created

```yaml
---
kind: configuration/kubernetes-master
name: default
provider: aws
specification:
  storage:
    name: epiphany-cluster-volume
    path: /
    enable: true
    capacity: 50
```

#### Additional configuration

If `provider: aws` is specified, EFS storage is always created and can be used with persistent volumes created by the 
user. It is possible to create a separate EFS and use it. For more information check Kubernetes 
[NFS](https://kubernetes.io/docs/concepts/storage/volumes/#nfs) storage documentation. There is another way
to use EFS by [Amazon EFS CSI driver](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html) but this approach
is not supported by Epiphany's AWS provider.

##### Persistent volume creation example

```yaml
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: epiphany-cluster-volume
spec:
  accessModes:
    - ReadWriteMany
  capacity:
    storage: 100Gi
  mountOptions:
    - hard
    - nfsvers=4.1
    - rsize=1048576
    - wsize=1048576
    - timeo=600
    - retrans=2
  nfs:
    path: /
    server: fs-xxxxxxxx.efs.eu-west-1.amazonaws.com
  storageClassName: defaultfs
  volumeMode: Filesystem
```
