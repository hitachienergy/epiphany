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

TODO

### Promote cluster to multi-master (HA) mode

This test create cluster with K8s component with single master and promotes it to multi-master (HA) mode, verifies completion, and then destroys cluster.

TODO

### Upgrade cluster with multi-master (HA) K8s

This test creates cluster in multi-master (HA) mode using release X and updates it to release / branch Y, verifies completion, and then destroys cluster.

TODO

### Create single machine environment

This test creates epiphany environment down-sized to single machine, verifies completion, and then destroys that machine.

TODO

### Create air-gaped cluster

This test prepares prerequisites for air-gaped installation, creates VMs and cuts them out from internet access, and then create fresh cluster from scratch, verifies completion, and then destroys cluster.

TODO

[develop-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/304
[develop-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/305
[develop-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/307
[develop-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/306
[develop-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/308

[07x-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/96/415
[07x-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/96/416
[07x-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/96/418
[07x-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/96/417
[07x-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/96/419

[06x-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/56/208
[06x-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/56/209
[06x-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/56/211
[06x-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/56/210
[06x-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/56/212

[05x-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/64/255
[05x-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/64/256
[05x-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/64/258
[05x-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/64/257
[05x-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/64/259

[04x-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/69/277
[04x-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/69/278
[04x-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/69/280
[04x-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/69/279
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
