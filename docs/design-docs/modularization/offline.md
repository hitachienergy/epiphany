# Offline modes in modularised Epiphany

## Context

Due to ongoing modularization process and introduction of middleware modules we need to decide how modules would obtain required dependencies for “offline” mode.

This document will describe installation and upgrade modes and will discuss ways to implement whole process considered during design process. 

## Assumptions
Each module has access to the “/shared” directory. Most wanted way to use modules is via “e” command line app.

## Installation modes

There are 2 main identified ways (each with 2 mutations) to install Epiphany cluster. 
 * Online - it means that one machine in a cluster has access to public internet. We would call this machine repository machine, and that scenario would be named "Jump Host". A specific scenario in this group is when all machines have access to internet. We are not really interested in that scenario because in all scenarios we want all cluster machines to download required elements from repository machine. We would call this scenario "Full Online"
 * Offline - it means that none of machines in a cluster have access to public internet. There are also two versions of this scenario. First version assumes that installation process is initialized on operators machine (i.e.: his/her laptop). We would call this scenario "Bastion v1". Second scenario is when all installation initialization process is executed directly from "Downloading Machine". We would call that scenario "Bastion v2". 

Following diagrams present high-level overview of those 4 scenarios: 

![Jump Host](./installation-modes/jump-host.png)

![Full Online](./installation-modes/full-online.png)

![Bastion v1](./installation-modes/bastion-v1.png)

![Bastion v2](./installation-modes/bastion-v2.png)

## Key machines

Described in the previous section scenarios show that there is couple machine roles identified in installation process. Following list explains those roles in more details.  

 * Repository - key role in whole lifecycle process. This is central cluster machine containing all the dependencies, providing images repository for the cluster, etc. 
 * Cluster machine - common cluster member providing computational resources to middleware being installed on it. This machine has to be able to see Repository machine. 
 * Downloading machine - this is a temporary machine required to download OS packages for the cluster. This is known process in which we download OS packages on a machine with access to public internet, and then we transfer those packages to Repository machine on which they are accessible to all the cluster machines. 
 * Laptop - terminal machine for a human operator to work on. There is no formal requirement for this machine to exist or be part of process. All operations performed on that machine could be performed on Repository or Downloading machine.  

## Downloading

This section describes identified ways to provide dependencies to cluster. There is 6 identified ways. All of them are described in following subsections with pros and cons.  

### Option 1
Docker image for each module has all required binaries embedded in itself during build process.

#### Pros
* There is no “download requirements” step.
* Each module has all requirements ensured on build stage.

#### Cons
* Module image is heavy.
* Possible licensing issues.
* Unknown versions of OS packages. 

### Option 2
There is separate docker image with all required binaries for all modules embedded in itself during build process. 

#### Pros
* There is no “download requirements” step.
* All requirements are stored in one image.

#### Cons
* Image would be extremely large.
* Possible licensing issues.
* Unknown versions of OS packages.

### Option 3
There is separate “dependencies” image for each module containing just dependencies. 

#### Pros
* There is no “download requirements” step.
* Module image itself is still relatively small.
* Requirements are ensured on build stage.

#### Cons
* “Dependencies” image is heavy.
* Possible licensing issues.
* Unknown versions of OS packages.

### Option 4
Each module has “download requirements” step and downloads requirements to some directory.

#### Pros
* Module is responsible for downloading its requirements on its own.
* Already existing “export/import” CLI feature would be enough.

#### Cons
* Offline upgrade process might be hard.
* Each module would perform the download process a bit differently.

### Option 5
Each module has “download requirements” step and downloads requirements to docker named volume.

#### Pros
* Module is responsible for downloading its requirements on its own.
* Generic docker volume practices could be used. 

#### Cons
* Offline upgrade process might be hard.
* Each module would perform the download process a bit differently.

### Option 6
Each module contains “requirements” section in its configuration, but there is one single module downloading requirements for all modules.

#### Pros
* Module is responsible for creation of BOM and single “downloader” container satisfies needs of all the modules.
* Centralised downloading process.
* Manageable offline installation process.

#### Cons
* Yet another “module”

### Options discussion
* Options 1, 2 and 3 are probably unelectable due to licenses of components and possibly big or even huge size of produced images.
* Main issue with options 1, 2 and 3 is that it would only work for containers and binaries but not OS packages as these are dependent on the targeted OS version and installation. This is something we cannot foresee or bundle for.
* Options 4 and 5 will introduce possibly a bit of a mess related to each module managing downloads on its own. Also upgrade process in offline mode might be problematic due to burden related to provide new versions for each module separately.
* Option 6 sounds like most flexible one.
