# Basic Infra ModuleS  VS Epicli Infra

## Basic overview

This represents the current status on: 05-25-2021

:heavy_check_mark: : Available
:x: : Not available
:heavy_exclamation_mark: Check the notes

| | | Epicli Azure | Epicli AWS | Azure BI |  AWS BI |
| - | - | - | - | - | - |
| Network | Virtual network | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| | Private subnets | :heavy_exclamation_mark: | :heavy_exclamation_mark: | :heavy_check_mark: | :heavy_check_mark: |
| | Public subnets | :heavy_exclamation_mark: | :heavy_exclamation_mark: | :heavy_check_mark: | :heavy_check_mark: |
| | Security groups with rules | :heavy_check_mark: | :heavy_check_mark: | :x: | :heavy_check_mark: |
| | Possibility for bastian host | :x: | :x: | :heavy_check_mark: | :heavy_check_mark: |
| | Possibility to connect to other infra (EKS, AKS) | :x: | :x: | :heavy_check_mark: | :heavy_check_mark: |
| VM | "Groups" with similar configuration | :heavy_check_mark: | :heavy_exclamation_mark: | :heavy_check_mark: | :heavy_check_mark: |
| | Data disks | :x: | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Easy configuration | | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: |

## Notes

- On Epicli AWS/Azure infrastructure we can either have a cluster with private or public subnets. As public IP`s can only be applied cluster wide and not on a VM "group" basis.
- On Epicli AWS we use Auto Scaling Groups to represent groups of similar VM`s. This approach however has lots of issues when it comes to scaling the group/component.

## Missing for Modules

1: Currently the Azure BI module does not have a way to inplement security groups per subnets with rules configuration
2: Both BI modules currently only gives a default configuration, which makes it hard to create a full component layout for a full cluster.
