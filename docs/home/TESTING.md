# Testing

This documentation describe approach in testing for open-source project 'epiphany-platform'.
In this section you can find tests status. 

## Status

### Create cluster

This test create fresh cluster from scratch with all components, verifies completion, and then destroys cluster.  

| Brench/Release | Init                      | OS     | AWS Status           | Azure Status           |
| :---           | :---:                     | :---:  | :---:                | :---:                  |
| develop        | ![develop-apply-init-prepare] | RedHat | ![develop-apply-rh-aws]  | ![develop-apply-rh-azure]  |
|                |                           | Ubuntu | ![develop-apply-ubu-aws] | ![develop-apply-ubu-azure] |
| 0.7.x          | ![07x-apply-init-prepare] | RedHat | ![07x-apply-rh-aws]  | ![07x-apply-rh-azure]  |
|                |                           | Ubuntu | ![07x-apply-ubu-aws] | ![07x-apply-ubu-azure] |
| 0.6.x          | ![06x-apply-init-prepare] | RedHat | ![06x-apply-rh-aws]  | ![06x-apply-rh-azure]  |
|                |                           | Ubuntu | ![06x-apply-ubu-aws] | ![06x-apply-ubu-azure] |
| 0.5.x          | ![05x-apply-init-prepare] | RedHat | ![05x-apply-rh-aws]  | ![05x-apply-rh-azure]  |
|                |                           | Ubuntu | ![05x-apply-ubu-aws] | ![05x-apply-ubu-azure] |
| 0.4.x          | ![04x-apply-init-prepare] | RedHat | ![04x-apply-rh-aws]  | ![04x-apply-rh-azure]  |
|                |                           | Ubuntu | ![04x-apply-ubu-aws] | ![04x-apply-ubu-azure] |

### Upgrade cluster

This test creates cluster using release X and upgrades it to release / branch Y, verifies completion, and then destroys cluster.

| From Release | To Branch/Release | OS     | AWS Status                     | Azure Status                     |
| :---         | :---:             | :---:  | :---:                          | :---:                            |
| 0.4.x        | 0.7.x             | RedHat | ![04x-07x-upgrade-rh-aws]      | ![04x-07x-upgrade-rh-azure]      |
|              |                   | Ubuntu | ![04x-07x-upgrade-ubu-aws]     | ![04x-07x-upgrade-ubu-azure]     |
| 0.5.x        | 0.7.x             | RedHat | ![05x-07x-upgrade-rh-aws]      | ![05x-07x-upgrade-rh-azure]      |
|              |                   | Ubuntu | ![05x-07x-upgrade-ubu-aws]     | ![05x-07x-upgrade-ubu-azure]     |
| 0.6.x        | 0.7.x             | RedHat | ![06x-07x-upgrade-rh-aws]      | ![06x-07x-upgrade-rh-azure]      |
|              |                   | Ubuntu | ![06x-07x-upgrade-ubu-aws]     | ![06x-07x-upgrade-ubu-azure]     |
| 0.4.x        | develop           | RedHat | ![04x-develop-upgrade-rh-aws]  | ![04x-develop-upgrade-rh-azure]  |
|              |                   | Ubuntu | ![04x-develop-upgrade-ubu-aws] | ![04x-develop-upgrade-ubu-azure] |
| 0.5.x        | develop           | RedHat | ![05x-develop-upgrade-rh-aws]  | ![05x-develop-upgrade-rh-azure]  |
|              |                   | Ubuntu | ![05x-develop-upgrade-ubu-aws] | ![05x-develop-upgrade-ubu-azure] |
| 0.6.x        | develop           | RedHat | ![06x-develop-upgrade-rh-aws]  | ![06x-develop-upgrade-rh-azure]  |
|              |                   | Ubuntu | ![06x-develop-upgrade-ubu-aws] | ![06x-develop-upgrade-ubu-azure] |

### Create cluster with multi-master (HA) K8s

This test create fresh cluster from scratch with K8s component in multi-master (HA) mode, verifies completion, and then destroys cluster.

| Brench/Release                  | OS             | AWS Status                      | Azure Status                      |
| :---                            | :---:          | :---:                           | :---:                             |
| develop                         | RedHat         | ![develop-apply-k8s-ha-rh-aws]  | ![develop-apply-k8s-ha-rh-azure]  |
|                                 | Ubuntu         | ![develop-apply-k8s-ha-ubu-aws] | ![develop-apply-k8s-ha-ubu-azure] |
| 0.7.x                           | RedHat         | ![07x-apply-k8s-ha-rh-aws]      | ![07x-apply-k8s-ha-rh-azure]      |
|                                 | Ubuntu         | ![07x-apply-k8s-ha-ubu-aws]     | ![07x-apply-k8s-ha-ubu-azure]     |
| 0.6.x                           | RedHat         | ![06x-apply-k8s-ha-rh-aws]      | ![06x-apply-k8s-ha-rh-azure]      |
| (init ![06x-apply-k8s-ha-init]) | Ubuntu         | ![06x-apply-k8s-ha-ubu-aws]     | ![06x-apply-k8s-ha-ubu-azure]     |

### Promote cluster to multi-master (HA) mode

This test create cluster with K8s component with single master and promotes it to multi-master (HA) mode, verifies completion, and then destroys cluster.

| Brench/Release | OS             | AWS Status                     | | | Azure Status                 | | |
| :---           | :---:          | :---: | :---: | :---: | :---: | :---: | :---:                             |
| :---           | :---:          | **apply** | **promote** | **scale** | **apply** | **promote** | **scale** |
| develop        | RedHat         | ![develop-apply-promote-apply-rh-aws]  | ![develop-apply-promote-promote-rh-aws]  | ![develop-apply-promote-scale-rh-aws]  | ![develop-apply-promote-apply-rh-azure]  | ![develop-apply-promote-promote-rh-azure]  | ![develop-apply-promote-scale-rh-azure]  | 
|                | Ubuntu         | ![develop-apply-promote-apply-ubu-aws] | ![develop-apply-promote-promote-ubu-aws] | ![develop-apply-promote-scale-ubu-aws] | ![develop-apply-promote-apply-ubu-azure] | ![develop-apply-promote-promote-ubu-azure] | ![develop-apply-promote-scale-ubu-azure] | 
| 0.7.x          | RedHat         | ![07x-apply-promote-apply-rh-aws]      | ![07x-apply-promote-promote-rh-aws]      | ![07x-apply-promote-scale-rh-aws]      | ![07x-apply-promote-apply-rh-azure]      | ![07x-apply-promote-promote-rh-azure]      | ![07x-apply-promote-scale-rh-azure]      | 
|                | Ubuntu         | ![07x-apply-promote-apply-ubu-aws]     | ![07x-apply-promote-promote-ubu-aws]     | ![07x-apply-promote-scale-ubu-aws]     | ![07x-apply-promote-apply-ubu-azure]     | ![07x-apply-promote-promote-ubu-azure]     | ![07x-apply-promote-scale-ubu-azure]     | 
| 0.6.x          | RedHat         | ![06x-apply-promote-apply-rh-aws]      | ![06x-apply-promote-promote-rh-aws]      | ![06x-apply-promote-scale-rh-aws]      | ![06x-apply-promote-apply-rh-azure]      | ![06x-apply-promote-promote-rh-azure]      | ![06x-apply-promote-scale-rh-azure]      | 
|                | Ubuntu         | ![06x-apply-promote-apply-ubu-aws]     | ![06x-apply-promote-promote-ubu-aws]     | ![06x-apply-promote-scale-ubu-aws]     | ![06x-apply-promote-apply-ubu-azure]     | ![06x-apply-promote-promote-ubu-azure]     | ![06x-apply-promote-scale-ubu-azure]     | 


### Upgrade cluster with multi-master (HA) K8s

This test creates cluster in multi-master (HA) mode using release X and updates it to release / branch Y, verifies completion, and then destroys cluster.

:bangbang: missing :bangbang:

### Create single machine environment

This test creates epiphany environment down-sized to single machine, verifies completion, and then destroys that machine.

| Brench/Release |  OS     | AWS Status               | Azure Status               |
| :---           |  :---:  | :---:                    | :---:                      |
| develop        | RedHat  | ![develop-single-rh-aws]  | ![develop-single-rh-azure]  |
|                |  Ubuntu | ![develop-single-ubu-aws] | ![develop-single-ubu-azure] |
| 0.7.x          |  RedHat | ![07x-single-rh-aws]      | ![07x-single-rh-azure]      |
|                |  Ubuntu | ![07x-single-ubu-aws]     | ![07x-single-ubu-azure]     |
| 0.6.x          |  RedHat | ![06x-single-rh-aws]      | ![06x-single-rh-azure]      |
|                |  Ubuntu | ![06x-single-ubu-aws]     | ![06x-single-ubu-azure]     |
| 0.5.x          |  RedHat | ![05x-single-rh-aws]      | ![05x-single-rh-azure]      |
|                |  Ubuntu | ![05x-single-ubu-aws]     | ![05x-single-ubu-azure]     |
| 0.4.x          |  RedHat | ![04x-single-rh-aws]      | ![04x-single-rh-azure]      |
|                |  Ubuntu | ![04x-single-ubu-aws]     | ![04x-single-ubu-azure]     |

### Create air-gaped cluster

This test prepares prerequisites for air-gaped installation, creates VMs and cuts them out from internet access, and then create fresh cluster from scratch, verifies completion, and then destroys cluster.

| Brench/Release | Prepare                    | OS     | Download Requirements           | AWS Status                    | Azure Status                  |
| :---           | :---:                      | :---:  | :---:                           | :---:                         | :---:                         |
| develop        | ![develop-offline-prepare] | RedHat | ![develop-offline-download-rh]  | ![develop-offline-rh-aws]     | ![develop-offline-rh-azure]   |
|                |                            | Centos | :bangbang: missing :bangbang:   | :bangbang: missing :bangbang: | :bangbang: missing :bangbang: |
|                |                            | Ubuntu | ![develop-offline-download-ubu] | ![develop-offline-ubu-aws]    | ![develop-offline-ubu-azure]  |
| 0.7.x          | ![07x-offline-prepare]     | RedHat | ![07x-offline-download-rh]      | ![07x-offline-rh-aws]         | ![07x-offline-rh-azure]       |
|                |                            | Centos | :bangbang: missing :bangbang:   | :bangbang: missing :bangbang: | :bangbang: missing :bangbang: |
|                |                            | Ubuntu | ![07x-offline-download-ubu]     | ![07x-offline-ubu-aws]        | ![07x-offline-ubu-azure]      |
| 0.6.x          | ![06x-offline-prepare]     | RedHat | ![06x-offline-download-rh]      | ![06x-offline-rh-aws]         | ![06x-offline-rh-azure]       |
|                |                            | Centos | :bangbang: missing :bangbang:   | :bangbang: missing :bangbang: | :bangbang: missing :bangbang: |
|                |                            | Ubuntu | ![06x-offline-download-ubu]     | ![06x-offline-ubu-aws]        | ![06x-offline-ubu-azure]      |
| 0.5.x          | ![05x-offline-prepare]     | RedHat | ![05x-offline-download-rh]      | ![05x-offline-rh-aws]         | ![05x-offline-rh-azure]       |
|                |                            | Centos | :bangbang: missing :bangbang:   | :bangbang: missing :bangbang: | :bangbang: missing :bangbang: |
|                |                            | Ubuntu | ![05x-offline-download-ubu]     | ![05x-offline-ubu-aws]        | ![05x-offline-ubu-azure]      |
| 0.4.x          | ![04x-offline-prepare]     | RedHat | ![04x-offline-download-rh]      | ![04x-offline-rh-aws]         | ![04x-offline-rh-azure]       |
|                |                            | Centos | :bangbang: missing :bangbang:   | :bangbang: missing :bangbang: | :bangbang: missing :bangbang: |
|                |                            | Ubuntu | ![04x-offline-download-ubu]     | ![04x-offline-ubu-aws]        | ![04x-offline-ubu-azure]      |

[develop-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/304
[07x-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/96/415
[06x-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/56/208
[05x-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/64/255
[04x-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/69/277

[develop-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/305
[develop-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/306
[07x-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/96/416
[07x-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/96/417
[06x-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/56/209
[06x-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/56/210
[05x-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/64/256
[05x-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/64/257
[04x-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/69/278
[04x-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/69/279

[develop-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/307
[develop-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/308
[07x-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/96/418
[07x-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/96/419
[06x-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/56/211
[06x-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/56/212
[05x-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/64/258
[05x-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/64/259
[04x-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/69/280
[04x-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/69/281

[04x-07x-upgrade-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/97/420   
[04x-07x-upgrade-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/97/421
[05x-07x-upgrade-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/98/424
[05x-07x-upgrade-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/98/425
[06x-07x-upgrade-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/99/428
[06x-07x-upgrade-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/99/429
[04x-develop-upgrade-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/92/399
[04x-develop-upgrade-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/92/400
[05x-develop-upgrade-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/94/406
[05x-develop-upgrade-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/94/407
[06x-develop-upgrade-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/95/411
[06x-develop-upgrade-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/95/412

[04x-07x-upgrade-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/97/422
[04x-07x-upgrade-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/97/423
[05x-07x-upgrade-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/98/426
[05x-07x-upgrade-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/98/427
[06x-07x-upgrade-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/99/430
[06x-07x-upgrade-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/99/431
[04x-develop-upgrade-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/92/401
[04x-develop-upgrade-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/92/402
[05x-develop-upgrade-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/94/408
[05x-develop-upgrade-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/94/409
[06x-develop-upgrade-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/95/413
[06x-develop-upgrade-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/95/414

[develop-apply-k8s-ha-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/77/310
[develop-apply-k8s-ha-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/77/311
[07x-apply-k8s-ha-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/100/432
[07x-apply-k8s-ha-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/100/433
[06x-apply-k8s-ha-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/59/223
[06x-apply-k8s-ha-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/59/224

[develop-apply-k8s-ha-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/77/312
[develop-apply-k8s-ha-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/77/313
[07x-apply-k8s-ha-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/100/434
[07x-apply-k8s-ha-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/100/435
[06x-apply-k8s-ha-init]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/59/222
[06x-apply-k8s-ha-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/59/225
[06x-apply-k8s-ha-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/59/226

[develop-apply-promote-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/314
[develop-apply-promote-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/317
[07x-apply-promote-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/436
[07x-apply-promote-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/439
[06x-apply-promote-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/238
[06x-apply-promote-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/244

[develop-apply-promote-promote-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/315
[develop-apply-promote-promote-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/318
[07x-apply-promote-promote-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/437
[07x-apply-promote-promote-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/440
[06x-apply-promote-promote-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/239
[06x-apply-promote-promote-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/245

[develop-apply-promote-scale-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/316
[develop-apply-promote-scale-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/319
[07x-apply-promote-scale-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/438
[07x-apply-promote-scale-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/441
[06x-apply-promote-scale-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/240
[06x-apply-promote-scale-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/246

[develop-apply-promote-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/320
[develop-apply-promote-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/323
[07x-apply-promote-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/442
[07x-apply-promote-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/445
[06x-apply-promote-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/241
[06x-apply-promote-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/247

[develop-apply-promote-promote-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/321
[develop-apply-promote-promote-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/324
[07x-apply-promote-promote-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/443
[07x-apply-promote-promote-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/446
[06x-apply-promote-promote-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/242
[06x-apply-promote-promote-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/248

[develop-apply-promote-scale-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/322
[develop-apply-promote-scale-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/78/325
[07x-apply-promote-scale-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/444
[07x-apply-promote-scale-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/101/447
[06x-apply-promote-scale-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/243
[06x-apply-promote-scale-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/62/249

[develop-single-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/79/326
[develop-single-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/79/327
[07x-single-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/102/448
[07x-single-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/102/449
[06x-single-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/60/227
[06x-single-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/60/228
[05x-single-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/66/262
[05x-single-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/66/263
[04x-single-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/72/293
[04x-single-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/72/294

[develop-single-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/79/328
[develop-single-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/79/329
[07x-single-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/102/450
[07x-single-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/102/451
[06x-single-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/60/229
[06x-single-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/60/230
[05x-single-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/66/264
[05x-single-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/66/265
[04x-single-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/72/295
[04x-single-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/72/296

[develop-offline-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/80/330
[07x-offline-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/103/452
[06x-offline-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/61/231
[05x-offline-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/67/266
[04x-offline-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/70/282

[develop-offline-download-rh]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/80/332
[develop-offline-download-ubu]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/80/331
[07x-offline-download-rh]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/103/454
[07x-offline-download-ubu]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/103/453
[06x-offline-download-rh]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/61/233
[06x-offline-download-ubu]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/61/232
[05x-offline-download-rh]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/67/268
[05x-offline-download-ubu]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/67/267
[04x-offline-download-rh]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/70/284
[04x-offline-download-ubu]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/70/283

[develop-offline-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/80/335
[develop-offline-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/80/336
[07x-offline-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/103/457
[07x-offline-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/103/458
[06x-offline-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/61/236
[06x-offline-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/61/237
[05x-offline-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/67/271
[05x-offline-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/67/272
[04x-offline-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/70/287
[04x-offline-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/70/288

[develop-offline-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/80/334
[develop-offline-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/80/333
[07x-offline-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/103/456
[07x-offline-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/103/455
[06x-offline-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/61/235
[06x-offline-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/61/234
[05x-offline-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/67/270
[05x-offline-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/67/269
[04x-offline-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/70/286
[04x-offline-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/70/285
