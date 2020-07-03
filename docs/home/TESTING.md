# Testing

This documentation describe approach in testing for open-source project 'epiphany-platform'.
In this section you can find tests status. 

## Status

### Cluster creation

This test create fresh cluster from scratch with all components, verifies completion, and then destroys cluster.  

| Brench/Release | Init                      | OS     | AWS Status           | Azure Status           |
| :---           | :---:                     | :---:  | :---:                | :---:                  |
| develop        | ![develop-apply-init-prepare] | RedHat | ![develop-apply-rh-aws]  | ![develop-apply-rh-azure]  |
|                |                           | Ubuntu | ![develop-apply-ubu-aws] | ![develop-apply-ubu-azure] |

[develop-apply-init-prepare]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/304
[develop-apply-rh-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/305
[develop-apply-rh-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/307
[develop-apply-ubu-aws]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/306
[develop-apply-ubu-azure]: https://abb-epiphany.vsrm.visualstudio.com/_apis/public/Release/badge/ce756f3f-4d59-41c4-983e-e8643138cd4e/76/308
