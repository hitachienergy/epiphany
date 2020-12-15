# memory-info

Reproduces what the kubelet does to calculate 'memory.available' relative to root cgroup.
It also calculates and shows other memory related info which helps you choose values
for kubelet configuration parameters (e.g. kubeReserved and systemReserved).

The value for 'memory.available' is derived from the cgroupfs instead of tools like free.

## Available options

```bash
-a, --clear-all-caches
    clear page cache and reclaimable slab objects (not recommended in production)

-p, --clear-page-cache
    clear page cache only

-s, --short
    less information

-v, --verbose
    more information
```

## Example usage

```bash
$ ./memory-info.sh --clear-all-caches
Clearing OS caches (page cache + reclaimable slab objects): sync; sysctl -w vm.drop_caches=3
vm.drop_caches = 3
---
memory capacity: 3876 MB
---
cgroup based memory info (used by k8s)
  available: 2990 MB
  working set: 886 MB
  usage: 1372 MB
---
cgroup: docker.service
  working set: 194 MB
  resident set size: 357 MB
  usage: 374 MB

cgroup: kubelet.service
  working set: 31 MB
  resident set size: 34 MB
  usage: 38 MB

cgroup: kubepods
  working set: 372 MB
  resident set size: 450 MB
  usage: 472 MB

cgroup: system.slice
  working set: 433 MB
  resident set size: 731 MB
  usage: 802 MB

cgroup: user.slice
  working set: 168 MB
  resident set size: 168 MB
  usage: 183 MB
---
/proc/meminfo based: free -m
              total        used        free      shared  buff/cache   available
Mem:           3876         818        2308           1         749        2954

--- calculations ---
docker.service + kubelet.service cgroups working set: 225 MB
meminfo working set: 921 MB (23.78%)
estimated system working set: 156 MB
estimated system + docker + kubelet working set: 381 MB

memory available delta [cgroup - meminfo]: 35 MB

--- limits ---
kubepods cgroup memory.limit: 2852 MB
kubelet.evictionHard.memory.available: 200Mi
computed allocatable memory for pods: 2652 MB (14.03% in use)
---
Load average: 0.33 0.22 0.26
```
