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

### Rook/Ceph General Configuration

To add Rook/Ceph support in Epiphany you need to add to your cluster configuration two elements:
- Storage (for cloud deployments - can be automatically created by Epiphany)
- Rook/Ceph

Adding the storage is described below in separate sections for Azure, AWS and on premise environments. Rook/Ceph configuration in Epiphany is described after add disk paragraphs.

#### Parameter `enable_controller_attach_detach`

Rook requires Kubelet parameter `--enable-controller-attach-detach` set to `true`. From Epiphany v2.0.1 by default this parameter is set to `true`. Users who would like to change its value, can achieve that by modifying `specification.advanced.enable_controller_attach_detach` setting in `configuration/kubernetes-master` doc.
*Note*: In Epiphany v2.0.0 `--enable-controller-attach-detach` parameter is set by default to `false`. In order to change its value, manual steps on each of affected Kubernetes node are required:
- modify file `/var/lib/kubelet/kubeadm-flags.env` by removing attach-detach flag
- add flag to `/var/lib/kubelet/config.yaml` file and set its value to `true`
- restart kubelet with `systemctl restart kubelet`
See [Set Kubelet parameters via a config file](https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/) for more information about Kubelet parameters.

#### Create disks for Rook/Ceph Cluster Storage - Azure

To create Rook/Ceph Cluster Storage on Azure first you need to add empty disk resource to Kubernetes cluster in key `specification.additional_disks`, under `kind: infrastructure/virtual-machine` for configuration of kubernetes node machine:

```yaml
---
kind: infrastructure/virtual-machine
name: kubernetes-node-machine
provider: azure
based_on: kubernetes-node-machine
specification:
  storage_image_reference:
    ..
  storage_os_disk:
    disk_size_gb: 64
  additional_disks:
    - storage_account_type: Premium_LRS
      disk_size_gb: 128
```

#### Create disks for Rook/Ceph Cluster Storage - AWS

To define additional empty disk resources for Rook/Ceph Cluster Storage on AWS, use `specification.disks.additional_disks` under `kind: infrastructure/virtual-machine` for configuration of kubernetes node machine:
```yaml
---
kind: infrastructure/virtual-machine
title: Virtual Machine Infra
provider: aws
name: kubernetes-node-machine
specification:
  disks:
    additional_disks:
      - device_name: "/dev/sdb"
        volume_type: gp2
        volume_size: 64
        delete_on_termination: false
        encrypted: true
```
Currently Epiphany support the following parameters for `additional_disks` specification:
- device_name
- volume_type
- volume_size
- encrypted
- delete_on_termination
- tags

More information about AWS block devices and its parameters: [ebs_block_device](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance#ebs_block_device)


#### Create disks for Rook/Ceph Cluster Storage - On Prem

To add disks to Rook/Ceph Cluster Storage you need to attach first raw devices to Kubernetes nodes machines and all raw devices will be used as Rook/Ceph devices.

#### Rook/Ceph Configuration

To install Rook/Ceph, set `enabled` to `true` in your input manifest:

```yaml
---
kind: configuration/features
title: Features to be enabled/disabled
name: default
specification:
  features:
    ...
    - name: rook
      enabled: true
```

If you want to install rook and rook cluster in the namespace different than `rook-ceph`, you need to add key `rook_namespace` with desired namespace name as value like in the sample below.

```yaml
---
kind: configuration/rook
title: "Kubernetes Rook Config"
name: default
specification:
    rook_namespace: your-rook-namespace
```

Epiphany configuration file provides set of parameters that are used for Rook/Ceph installation with default values.
To override default values provided by Rook you need to adjust `configuration/rook` keys:
- `specification.operator_chart_values` - to override Rook Operator Helm Chart default values
- `specification.cluster_chart_values` - to override Rook Cluster Helm Chart default values

```yaml
---
kind: configuration/rook
title: "Kubernetes Rook Config"
name: default
specification:
    operator_chart_values: |
      ...
    cluster_chart_values: |
      ...
```
Values nested below the `operator_chart_values` and `cluster_chart_values` keys are respectively Helm Chart values for Rook Operator and Rook Ceph Cluster.
It is important to ensure that configuration of operator and chart values matches configuration of your cluster.

More information about Helm Chart values may be found:
- [Helm Operator](https://github.com/rook/rook/blob/master/Documentation/helm-operator.md)
- [Helm Ceph Cluster](https://github.com/rook/rook/blob/master/Documentation/helm-ceph-cluster.md)

Sample configuration files that can be used in Epiphany `configuration/rook`:
- [Helm Operator](https://raw.githubusercontent.com/rook/rook/v1.8.8/deploy/charts/rook-ceph/values.yaml)
- [Helm Ceph Cluster](https://raw.githubusercontent.com/rook/rook/v1.8.8/deploy/charts/rook-ceph-cluster/values.yaml)

More informations about Rook with Ceph storage may be found in the official Rook [documentation](https://rook.io/docs/rook/v1.8/).

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
