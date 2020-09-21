# Patching OS with running Epiphany components

This guide describes steps you have to perform to patch RHEL and Ubuntu operating systems in a way to not to interrupt working Epiphany components.

### Disclaimer

We provide a recommended way to patch your RHEL and Ubuntu operating systems. Before proceeding with patching the production environment we strongly recommend patching your test cluster first.  
This document will help you decide how you should patch your OS. This is not a step-by-step guide.

### Requirements

- The fresh, actual backup containing your all important data
- Verify if repositories are in the desired state. Details [here](#repositories)

# Table of contents

- [AWS](#aws)
- [AZURE](#azure)
- [Patching with Package Manager](#patching-with-package-manager)
  - [Repositories](#repositories)
  - [RHEL](#rhel)
  - [Ubuntu](#ubuntu)
- [Patching with external tools](#patching-with-external-tools)

## AWS

### Suggested OS images

For Epiphany v0.8 we recommend the following image (AMI):  

- RHEL: `RHEL-7.8_HVM_GA-20200225-x86_64-1-Hourly2-GP2` (kernel 3.10.0-1127.el7.x86_64),
- Ubuntu: `ubuntu-bionic-18.04-amd64-server-20200611` (kernel 5.3.0-1028-aws).

Note: For different supported OS versions this guide may be useful as well.

### Patching methods

AWS provides `Patch Manager` that automates the process of patching managed instances.  
Benefits:

- Automate patching
- Define approval rules
- Create patch baselines
- Monitor compliance

This feature is available via:

- console: [Systems Manager](https://console.aws.amazon.com/systems-manager/) > Instances & Nodes > [Patch Manager](https://console.aws.amazon.com/systems-manager/patch-manager)
- [AWS CLI](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-cli-commands.html)

For more information, refer to [AWS Systems Manager User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-patch.html).

## Azure

### Suggested OS images

For Epiphany v0.8 we recommend the following image (urn):  

- RHEL: `RHEL:7-RAW:7.7.2019090418` (kernel 3.10.0-1062.1.1.el7.x86_64),
- Ubuntu: `UbuntuServer:18.04-LTS:18.04.202006101` (kernel 5.3.0-1028-azure).

Note: For different supported OS versions this guide may be useful as well.

### Patching methods

Azure has `Update Management` solution in `Azure Automation`. It gives you visibility into update compliance across Azure and other clouds, and on-premises. The feature allows you to create scheduled deployments that orchestrate the installation of updates within a defined maintenance window.  
To manage updates that way please refer to [official documentation](https://docs.microsoft.com/en-us/azure/automation/update-management/update-mgmt-manage-updates-for-vm).

## Patching with OS specific package manager

The following commands can be executed in both clustered and non-clustered environments. In case of patching non-clustered environment, you have to schedule a maintenance window due to the required reboot after kernel patching.  

Note: Some of the particular patches may also require a system reboot.

If your environment is clustered then hosts should be patched one by one. Before proceeding with the next host be sure that the patched host is up and all its components are running.  
For information how to check state of specific Epiphany components, see [here](./MAINTENANCE.md).

### Repositories

Epiphany uses the repository role to provide all required packages. The role disables all existing repositories and provides a new one. After successful Epiphany deployment, official repositories should be re-enabled and Epiphany-provided repository should be disabled.

### RHEL

Verify if *epirepo* is disabled:  
`yum repolist epirepo`

Verify if repositories you want to use for upgrade are enabled:  
`yum repolist all`

List installed security patches:  
`yum updateinfo list security installed`

List available patches without installing them:  
`yum updateinfo list security available`

Grab more details about available patches:  
`yum updateinfo info security available` or specific patch: `yum updateinfo info security <patch_name>`

Install system security patches:  
`sudo yum update-minimal --sec-severity=critical,important --bugfix`

Install all patches and updates, not only flagged as critical and important:  
`sudo yum update`

You can also specify the exact bugfix you want to install or even which CVE vulnerability to patch, for example:  
`sudo yum update --cve CVE-2008-0947`

Available options:

```shell
  --advisory=ADVS, --advisories=ADVS
                        Include packages needed to fix the given advisory, in updates
  --bzs=BZS             Include packages needed to fix the given BZ, in updates
  --cves=CVES           Include packages needed to fix the given CVE, in updates
  --sec-severity=SEVS, --secseverity=SEVS
                        Include security relevant packages matching the severity, in updates
```

**Additional information**
Red Hat provides notifications about security flaws that affect its products in the form of security advisories. For more information, see [here](https://access.redhat.com/security/updates/advisory).

### Ubuntu

For automated security patches Ubuntu uses unattended-upgrade facility. By default it runs every day. To verify it on your system, execute:  
`dpkg --list unattended-upgrades`
`cat /etc/apt/apt.conf.d/20auto-upgrades | grep Unattended-Upgrade`

For information how to change Unattended-Upgrade configuration, see [here](https://github.com/mvo5/unattended-upgrades/blob/master/README.md).

The following steps will allow you to perform an upgrade manually.  

Update your local repository cache:  
`sudo apt update`

Verify if *epirepo* is disabled:  
`apt-cache policy | grep epirepo`

Verify if repositories you want to use for upgrade are enabled:  
`apt-cache policy`

List available upgrades without installing them:  
`apt-get upgrade -s`

List available security patches:  
`sudo unattended-upgrade -d --dry-run`

Install system security patches:  
`sudo unattended-upgrade -d`

Install all patches and updates with dependencies:  
`sudo apt-get dist-upgrade`

Verify if your system requires a reboot after an upgrade (check if file exists):  
`test -e /var/run/reboot-required && echo reboot required || echo reboot not required`

**Additional information**
Canonical provides notifications about security flaws that affect its products in the form of security notices. For more information, see [here](https://ubuntu.com/security/notices).

## Patching with external tools

Solutions are available to perform kernel patching without system reboot.  

- [Red Hat kpatch](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/kernel_administration_guide/applying_patches_with_kernel_live_patching) only for RHEL,
- [Canonical Livepatch Service](https://ubuntu.com/livepatch) only for Ubuntu,
- [KernelCare](https://www.kernelcare.com/) - third-party software. Available also in [AWS Marketplace](https://aws.amazon.com/marketplace/pp/B085ZLFK7B) in SaaS model.

If you have a valid subscription for any of the above tools, we highly recommend using it to patch your systems.
