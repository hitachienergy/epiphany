# Patching OS with running Epiphany components

This guide describes steps you have to perform to patch RedHat systems in a way to don't interrupt working Epiphany components.

### Disclamer

We providing a recommended way to patch your RedHat systems. Before proceeding with patching the production environment we highly recommending performing an update of your test cluster first.  
This document will help you decide how you should patch your OS. This is not a step-by-step guide.

### Requirements

- The fresh, actual backup contains your all sensitive data

## AWS

### Suggested OS images

For Epiphany v0.8 we recommend the following image (AMI):  
`RHEL-7.8_HVM_GA-20200225-x86_64-1-Hourly2-GP2` which contain `3.10.0-1127.el7.x86_64` kernel version.

> Note: For different supported OS versions this guide may be useful as well.

### Patching methods

AWS provides `Patch Manager` for patching OSes. This option is available via:  
[Systems Manager](https://eu-central-1.console.aws.amazon.com/systems-manager/) > Instances & Nodes > [Patch Manager](https://eu-central-1.console.aws.amazon.com/systems-manager/patch-manager) and it has equivalent in [aws cli](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-cli-commands.html).  
To use AWS Patch Manager please use the following instruction: [link](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-how-it-works.html)  
This feature will let you automate patching your instances.  
Benefits:

```shell
- Automate Patching
- Define approval rules
- Create patch baselines
- Monitor compliance
```

We won't detail these aspects in this doc because they were already well covered by AWS in the above link.

AWS supports a bunch of paid solutions to perform kernel patching without system reboot.  
Examples: RedHat [kpatch](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/kernel_administration_guide/applying_patches_with_kernel_live_patching) or external tool from its partner [KernelCare](https://www.kernelcare.com/) which is available in [AWS Marketplace](https://aws.amazon.com/marketplace/pp/B085ZLFK7B) in SaaS model.  
If you have a valid subscription for any of the above tools, we highly recommend using it to patch your system.

## Azure

### Suggested OS images

For Epiphany v0.8 we recommend the following image (urn):  
`RHEL:7-RAW:7.7.2019090418` which contain `3.10.0-1062.1.1.el7.x86_64` kernel version.

> Note: For different supported OS versions this guide may be useful as well.

### Patching methods

Azure has dedicated solution update management called `Azure Automation` which include feature `Update Management`. It gives you visibility into update compliance across Azure and other clouds, and on-premises. The feature allows you to create scheduled deployments that orchestrate the installation of updates within a defined maintenance window.  
To manage updates that way please refer to [official documentation](https://docs.microsoft.com/en-us/azure/automation/update-management/update-mgmt-manage-updates-for-vm).

## Patching RedHat by Package Manager

The following commands can be executed in both clustered and non-clustered environments. In case of patching non-clustered environment you have to schedule a maintenance window due to required reboot after kernel patching.  

> Note: Some of the particular patches may also require a system reboot.

If your environment is clustered then hosts should be patched one by one. Before proceeding with the next host be sure that the patched host is up and all its components are running.  
Here you can find information how to check state of specific Epiphany components: [link](./MAINTENANCE.md).  
To verify your current Linux Kernel version use:  
`sudo uname -r`  
To list installed security patches use:  
`sudo yum updateinfo list security installed`  
To list available patches without installing them use:  
`sudo yum updateinfo list security available`  
To grab more details about available patch use:  
`sudo yum updateinfo info security available` or specify patch: `sudo yum updateinfo info security <patch_name>)`  
To install system security patches in RedHat system, execute:  
`sudo yum update-minimal --sec-severity=critical,important --bugfix`  
To install all patches and updates, not only flaged as critical and important, execute:  
`yum update`  
You can also specify the exact bugfix you want to install or even which CVE vulnerability to patch:  
Example: `yum update --cve CVE-2008-0947`  
Available options:

```shell
  --advisory=ADVS, --advisories=ADVS
                        Include packages needed to fix the given advisory, in updates
  --bzs=BZS             Include packages needed to fix the given BZ, in updates
  --cves=CVES           Include packages needed to fix the given CVE, in updates
  --sec-severity=SEVS, --secseverity=SEVS
                        Include security relevant packages matching the severity, in updates
```

## Additional information

RedHat offers an e-mail subscription for security issue notification. You can easily subscribe to the mailing list via [official site](https://www.redhat.com/mailman/listinfo/rhsa-announce)
