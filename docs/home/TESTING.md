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

This test creates cluster using release X and updates it to release / branch Y, verifies completion, and then destroys cluster.

TODO

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
