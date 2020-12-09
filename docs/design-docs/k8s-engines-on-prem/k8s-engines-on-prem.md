# ON-PREM KUBERNETES AUTOMATION RESEARCH RESULTS

## 1. KOPS

- cannot be used, because it's cloud-exclusive

## 2. KUBICORN

- cannot be used, because it's cloud-exclusive

## 3. RKE

### 3.1 DESIGN

- installed from a single statically-linked binary
- does not use kubeadm
- requires (only!) docker-ce to be pre-installed on all machines [requirements](https://rancher.com/docs/rke/latest/en/os/)
- uses "hyperkube-style" deployment

```
$ docker ps
CONTAINER ID        IMAGE                                                 COMMAND                  CREATED             STATUS              PORTS               NAMES
a717a88416b8        10.8.101.2:5000/rancher/calico-node                   "start_runit"            4 minutes ago       Up 4 minutes                            k8s_calico-node_calico-node-fm2lx_kube-system_110fc1df-053c-4e07-a6a9-d18b092c7689_0
6203b74014ff        10.8.101.2:5000/rancher/pause:3.1                     "/pause"                 4 minutes ago       Up 4 minutes                            k8s_POD_calico-node-fm2lx_kube-system_110fc1df-053c-4e07-a6a9-d18b092c7689_0
0f9d4b9f38fd        10.8.101.2:5000/rancher/hyperkube:v1.18.12-rancher1   "/opt/rke-tools/entr…"   5 minutes ago       Up 5 minutes                            kube-proxy
bd37f5d76216        10.8.101.2:5000/rancher/hyperkube:v1.18.12-rancher1   "/opt/rke-tools/entr…"   5 minutes ago       Up 5 minutes                            kubelet
81357e60baee        10.8.101.2:5000/rancher/hyperkube:v1.18.12-rancher1   "/opt/rke-tools/entr…"   5 minutes ago       Up 5 minutes                            kube-scheduler
3a0ca597e86c        10.8.101.2:5000/rancher/hyperkube:v1.18.12-rancher1   "/opt/rke-tools/entr…"   5 minutes ago       Up 5 minutes                            kube-controller-manager
abb0328793bf        10.8.101.2:5000/rancher/hyperkube:v1.18.12-rancher1   "/opt/rke-tools/entr…"   5 minutes ago       Up 5 minutes                            kube-apiserver
d6b3de42c623        10.8.101.2:5000/rancher/rke-tools:v0.1.66             "/docker-entrypoint.…"   6 minutes ago       Up 6 minutes                            etcd-rolling-snapshots
923998518d49        10.8.101.2:5000/rancher/coreos-etcd:v3.4.3-rancher1   "/usr/local/bin/etcd…"   6 minutes ago       Up 6 minutes                            etcd
```
```
NAME              STATUS   ROLES               AGE   VERSION
node/10.50.2.10   Ready    controlplane,etcd   68s   v1.18.12
node/10.50.2.11   Ready    controlplane,etcd   68s   v1.18.12
node/10.50.2.12   Ready    controlplane,etcd   68s   v1.18.12
node/10.50.2.20   Ready    worker              67s   v1.18.12
node/10.50.2.21   Ready    worker              67s   v1.18.12
node/10.50.2.22   Ready    worker              67s   v1.18.12

NAMESPACE       NAME                                           READY   STATUS      RESTARTS   AGE
ingress-nginx   pod/default-http-backend-5b564dd459-stjgz      1/1     Running     0          32s
ingress-nginx   pod/nginx-ingress-controller-blz4j             1/1     Running     0          32s
ingress-nginx   pod/nginx-ingress-controller-cj8nd             1/1     Running     0          32s
ingress-nginx   pod/nginx-ingress-controller-fqjdh             1/1     Running     0          32s
kube-system     pod/calico-kube-controllers-6c6fc476f6-82wzb   1/1     Running     0          48s
kube-system     pod/calico-node-7dz2m                          1/1     Running     0          47s
kube-system     pod/calico-node-cm5rc                          0/1     Running     0          47s
kube-system     pod/calico-node-dmwbz                          0/1     Running     0          47s
kube-system     pod/calico-node-kf6zb                          0/1     Running     0          47s
kube-system     pod/calico-node-nczbb                          0/1     Running     0          47s
kube-system     pod/calico-node-zjtmj                          1/1     Running     0          47s
kube-system     pod/coredns-5dd4dfcb45-lvlc4                   1/1     Running     0          10s
kube-system     pod/coredns-5dd4dfcb45-sj44t                   1/1     Running     0          44s
kube-system     pod/coredns-autoscaler-557f965569-4sbdd        1/1     Running     0          43s
kube-system     pod/metrics-server-77956db857-pdklq            1/1     Running     0          38s
kube-system     pod/rke-coredns-addon-deploy-job-2h25s         0/1     Completed   0          46s
kube-system     pod/rke-ingress-controller-deploy-job-9882t    0/1     Completed   0          36s
kube-system     pod/rke-metrics-addon-deploy-job-l47wt         0/1     Completed   0          41s
kube-system     pod/rke-network-plugin-deploy-job-xzrwp        0/1     Completed   0          56s
```

### 3.2 OFFLINE / AIR-GAPPED

- not fully supported / automated (but easy to implement)
- the list of required docker images can be obtained via `rke -q config -s`
- user needs to provide on-prem docker-registry
- no linux system packages (except for docker-ce with dependencies) are required / installed

### 3.3 CNI PLUGINS

supported:
- calico
- canal (default)
- flannel
- weave
- [custom plugins](https://rancher.com/docs/rke/latest/en/config-options/add-ons/network-plugins/custom-network-plugin-example/)

### 3.4. RESULTS

asciinema casts (reload page if cast doesn't work):
- [rke-centos](https://asciinema.org/a/378121)
- [rke-ubuntu](https://asciinema.org/a/378120)
- [rke-ubuntu-in-azure](https://asciinema.org/a/377768)

#### 3.4.1 UBUNTU

- docker-ce installed in `4m42.450s`
- v1.18.12 installed with no errors in `3m21.134s`
- upgraded with no errors to v1.19.4 in `5m21.850s`

#### 3.4.2 CENTOS

- docker-ce installed in `5m49.049s`
- v1.18.12 installed with no errors in `3m8.847s`
- upgraded with no errors to v1.19.4 in `4m31.851s`

#### 3.4.3 AZURE UBUNTU (ONLINE)

- docker-ce pre-installed during terraform provisioning (no data)
- v1.18.12 installed with no errors in `12m32.977s`
- upgraded with no errors to v1.19.4 in `16m55.058s`

### 3.5 PROS / CONS

PROS:
- installed using single statically-linked binary
- supports recent Kubernetes versions
- requires only docker-ce to be pre-installed
- downloading docker images is very simple to implement
- very fast, rke (with pre-installed docker-ce) installs or upgrades in ~5 minutes on 6-node KVM cluster
- very stable, rke did not fail even once during my tests
- cluster configuration file is intuitive and easy to understand
- good / easy-to-read documentation (I did not need to read the source code)
- extracts kubeconfig automatically

CONS:
- no script for downloading docker images and building docker registry automatically
- provides its own docker images

## 4. KUBESPRAY

### 4.1 DESIGN

- can be managed using pre-built docker images form [quay.io](https://quay.io/repository/kubespray/kubespray)
- ansible based
- uses kubeadm, the "classic" experience
- installs all required system packages automatically (including docker-ce)

```
NAME        STATUS   ROLES    AGE     VERSION
node/u1a1   Ready    master   3m15s   v1.17.13
node/u1a2   Ready    master   2m44s   v1.17.13
node/u1a3   Ready    master   2m44s   v1.17.13
node/u1b1   Ready    <none>   108s    v1.17.13
node/u1b2   Ready    <none>   108s    v1.17.13
node/u1b3   Ready    <none>   108s    v1.17.13

NAMESPACE     NAME                                             READY   STATUS    RESTARTS   AGE
kube-system   pod/calico-kube-controllers-74b9b94cfc-2mghd     1/1     Running   0          67s
kube-system   pod/calico-node-96rw7                            1/1     Running   1          88s
kube-system   pod/calico-node-gctfv                            1/1     Running   1          88s
kube-system   pod/calico-node-hl95t                            1/1     Running   1          88s
kube-system   pod/calico-node-m9kks                            1/1     Running   1          88s
kube-system   pod/calico-node-qn98z                            1/1     Running   1          88s
kube-system   pod/calico-node-x9864                            1/1     Running   1          88s
kube-system   pod/coredns-58b9c97c99-7qgnm                     1/1     Running   0          55s
kube-system   pod/coredns-58b9c97c99-9fx4m                     1/1     Running   0          51s
kube-system   pod/dns-autoscaler-77c78db666-w2kgx              1/1     Running   0          52s
kube-system   pod/kube-apiserver-u1a1                          1/1     Running   0          3m8s
kube-system   pod/kube-apiserver-u1a2                          1/1     Running   0          2m37s
kube-system   pod/kube-apiserver-u1a3                          1/1     Running   0          2m37s
kube-system   pod/kube-controller-manager-u1a1                 1/1     Running   0          3m8s
kube-system   pod/kube-controller-manager-u1a2                 1/1     Running   0          2m37s
kube-system   pod/kube-controller-manager-u1a3                 1/1     Running   0          2m37s
kube-system   pod/kube-proxy-2xxjh                             1/1     Running   0          108s
kube-system   pod/kube-proxy-4rps2                             1/1     Running   0          2m44s
kube-system   pod/kube-proxy-7zxbz                             1/1     Running   0          2m56s
kube-system   pod/kube-proxy-h2xmz                             1/1     Running   0          108s
kube-system   pod/kube-proxy-hm7lm                             1/1     Running   0          108s
kube-system   pod/kube-proxy-jsxl6                             1/1     Running   0          2m44s
kube-system   pod/kube-scheduler-u1a1                          1/1     Running   0          3m8s
kube-system   pod/kube-scheduler-u1a2                          1/1     Running   0          2m37s
kube-system   pod/kube-scheduler-u1a3                          1/1     Running   0          2m37s
kube-system   pod/kubernetes-dashboard-84bfd98759-hsrjk        1/1     Running   0          50s
kube-system   pod/kubernetes-metrics-scraper-79745547b-8g58c   1/1     Running   0          50s
kube-system   pod/nginx-proxy-u1b1                             1/1     Running   0          107s
kube-system   pod/nginx-proxy-u1b2                             1/1     Running   0          107s
kube-system   pod/nginx-proxy-u1b3                             1/1     Running   0          107s
kube-system   pod/nodelocaldns-4rdr7                           1/1     Running   0          51s
kube-system   pod/nodelocaldns-fmb5b                           1/1     Running   0          51s
kube-system   pod/nodelocaldns-kjx77                           1/1     Running   0          51s
kube-system   pod/nodelocaldns-lr4cf                           1/1     Running   0          51s
kube-system   pod/nodelocaldns-pvlwc                           1/1     Running   0          51s
kube-system   pod/nodelocaldns-tjwfr                           1/1     Running   0          51s
```

### 4.2 OFFLINE / AIR-GAPPED

- not fully supported / automated
- docker images and binary files (kubeadm, kubectl, ...) can be downloaded automatically
- the "download procedure" requires exising 2-node online cluster (sic!)
- the "download procedure" fails if there is no "/etc/kubernetes/" folder present on the machines (sic!)
- user needs to provide on-prem docker-registry and http server
- it's possible to use (automatically set) on-prem mirror repository for system packages (that completes the offline installation)

### 4.3 CNI PLUGINS

supported:
- calico (default)
- canal
- cilium
- flannel
- kube-ovn
- kube-router
- macvlan
- ovn4nfv
- weave

### 4.4 RESULTS

asciinema casts (reload page if cast doesn't work):
- [kubespray-centos](https://asciinema.org/a/377774)
- [kubespray-ubuntu](https://asciinema.org/a/377775)
- [kubespray-ubuntu-in-azure](https://asciinema.org/a/377776)

#### 4.4.1 UBUNTU

- v1.17.13 installed with no errors in `13m1.466s`
- upgrade to v1.18.10 failed repeatedly (no data)

#### 4.4.2 CENTOS

- v1.17.13 installed with no errors in `13m16.955s`
- upgraded with no errors to v1.18.10 in `11m6.016s`

#### 4.4.3 AZURE UBUNTU (ONLINE)

- v1.17.13 installed with no errors in `61m55.709s`
- upgraded with no errors to v1.18.10 in `59m58.529s`

### 4.5 PROS / CONS

PROS:
- extended list of supported CNI plugins
- uses generally-available docker images
- installs system packages automatically

CONS:
- latest release (2.14.2) does not support recent Kubernetes versions
- insane procedure for downloading docker images and files (requires a running online cluster!)
- no script for building docker registry automatically
- docker socket and full sudo privileges on the controller machine are required to run some of the ansible plays (sic!)
- installs system packages
- very slow
- upgrades are not completely stable
- bad documentation (I needed couple of hours of reading ansible code to understand what is going on)
- does not extract kubeconfig automatically

## 5. KUBEONE

### 5.1 DESIGN

- installed from a single statically-linked binary
- uses kubeadm, the "classic" experience
- installs all required system packages automatically (including docker-ce)
- executes bash snippets via ssh

```
NAME                  STATUS   ROLES    AGE     VERSION
node/u1a1.ubuntu.lh   Ready    master   2m58s   v1.18.12
node/u1a2.ubuntu.lh   Ready    master   2m19s   v1.18.12
node/u1a3.ubuntu.lh   Ready    master   84s     v1.18.12
node/u1b1.ubuntu.lh   Ready    <none>   64s     v1.18.12
node/u1b2.ubuntu.lh   Ready    <none>   57s     v1.18.12
node/u1b3.ubuntu.lh   Ready    <none>   64s     v1.18.12

NAMESPACE     NAME                                              READY   STATUS    RESTARTS   AGE
kube-system   pod/calico-kube-controllers-5cc64575d9-rhrn7      1/1     Running   0          77s
kube-system   pod/canal-8gpsd                                   2/2     Running   0          78s
kube-system   pod/canal-d4lqz                                   2/2     Running   0          64s
kube-system   pod/canal-k944p                                   2/2     Running   0          78s
kube-system   pod/canal-tfkh8                                   2/2     Running   0          78s
kube-system   pod/canal-vnd9b                                   2/2     Running   0          64s
kube-system   pod/canal-w4bwm                                   2/2     Running   0          57s
kube-system   pod/coredns-d6d746d5d-9d4kn                       1/1     Running   0          2m40s
kube-system   pod/coredns-d6d746d5d-wrcbz                       1/1     Running   0          2m40s
kube-system   pod/etcd-u1a1.ubuntu.lh                           1/1     Running   0          2m49s
kube-system   pod/etcd-u1a2.ubuntu.lh                           1/1     Running   0          2m7s
kube-system   pod/etcd-u1a3.ubuntu.lh                           0/1     Pending   0          1s
kube-system   pod/kube-apiserver-u1a1.ubuntu.lh                 1/1     Running   0          2m49s
kube-system   pod/kube-apiserver-u1a2.ubuntu.lh                 1/1     Running   0          2m7s
kube-system   pod/kube-apiserver-u1a3.ubuntu.lh                 1/1     Running   0          24s
kube-system   pod/kube-controller-manager-u1a1.ubuntu.lh        1/1     Running   1          2m49s
kube-system   pod/kube-controller-manager-u1a2.ubuntu.lh        1/1     Running   0          2m7s
kube-system   pod/kube-proxy-dk9k8                              1/1     Running   0          2m19s
kube-system   pod/kube-proxy-dnkx5                              1/1     Running   0          64s
kube-system   pod/kube-proxy-q4h7x                              1/1     Running   0          57s
kube-system   pod/kube-proxy-s2wzx                              1/1     Running   0          84s
kube-system   pod/kube-proxy-vddsl                              1/1     Running   0          64s
kube-system   pod/kube-proxy-vnhlm                              1/1     Running   0          2m40s
kube-system   pod/kube-scheduler-u1a1.ubuntu.lh                 1/1     Running   1          2m48s
kube-system   pod/kube-scheduler-u1a2.ubuntu.lh                 1/1     Running   0          2m7s
kube-system   pod/kube-scheduler-u1a3.ubuntu.lh                 1/1     Running   0          8s
kube-system   pod/machine-controller-7bfb85845-n4f5g            1/1     Running   0          56s
kube-system   pod/machine-controller-webhook-7bf5f89954-47qp7   1/1     Running   0          56s
kube-system   pod/metrics-server-5f75c7cb4f-gj4rq               1/1     Running   0          81s
kube-system   pod/node-local-dns-54vxf                          1/1     Running   0          64s
kube-system   pod/node-local-dns-7h5m8                          1/1     Running   0          64s
kube-system   pod/node-local-dns-7tsvf                          1/1     Running   0          82s
kube-system   pod/node-local-dns-c58zf                          1/1     Running   0          82s
kube-system   pod/node-local-dns-dvnbb                          1/1     Running   0          57s
kube-system   pod/node-local-dns-vsjpb                          1/1     Running   0          82s
```

### 5.2 OFFLINE / AIR-GAPPED

- not fully supported / automated (but provides at least a script to download docker images)
- user needs to provide on-prem docker-registry
- user needs to take care about system packages

### 5.3 CNI PLUGINS

supported:
- canal (default)
- weave

calico is only supported via "addon" [here](https://github.com/kubermatic/kubeone/pull/972/commits/9e89b3786836fe19f89f237757ea4a9363e6707c)

### 5.4 RESULTS

asciinema casts (reload page if cast doesn't work):
- [kubeone-centos](https://asciinema.org/a/377771)
- [kubeone-ubuntu](https://asciinema.org/a/377772)
- [kubeone-ubuntu-in-azure](https://asciinema.org/a/377773)

#### 5.4.1 UBUNTU

- v1.18.12 installed with no errors in `11m1.982s`
- upgraded with no errors to v1.19.4 in `10m49.110s`

#### 5.4.2 CENTOS

- v1.18.12 installed with no errors in `13m42.656s`
- upgraded with no errors to v1.19.4 in `10m28.346s`

#### 5.4.3 AZURE UBUNTU (ONLINE)

- v1.18.12 failed repeatedly (no data)
- nothing to upgrade (no data)

### 5.5 PROS / CONS

PROS:
- installed using single statically-linked binary
- supports recent Kubernetes versions
- uses generally-available docker images
- installs system packages automatically
- provides script for pulling and pushing docker images to local docker-registry (although it uses docker instead of skopeo)
- extracts kubeconfig automatically
- seems stable enough for on-prem usage

CONS:
- bad, hard-to-read / no-examples documentation (I had to read source code to understand how to configure on-prem cluster [here](https://github.com/kubermatic/kubeone/blob/v1.1.0/pkg/cmd/config.go))
- installs system packages
- poor cni support
- looks like a "ssh-engine" to run bash scripts

## 6. OTHERS

Things like on the list below are there as well, but usually such smaller projects have outdated Kubernetes or little to no development activity:

- [metalk8s](https://github.com/scality/metalk8s)
- [kube-ansible](https://github.com/kairen/kube-ansible)

## 7. CONSLUSIONS

Out of what we have here now:
- considering overall quality of the design, documentation, speed and stability the [rke](https://github.com/rancher/rke) seems to be clear winner
- [kubespray](https://github.com/kubernetes-sigs/kubespray) although the slowest seems to be better choice than [kubeone](https://github.com/kubermatic/kubeone), which tbh looks like a ssh-engine for running bash scripts
