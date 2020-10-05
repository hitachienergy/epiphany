# Modules

## Introduction

In version 0.8 of epiphany we are introducing modules. Modularisation of epiphany environment will result in: 
 * smaller code bases for separate areas, 
 * simpler and faster test process, 
 * interchangeability of elements providing similar functionality (eg.: different kubernetes providers), 
 * faster and more focused release cycle. 
 
Those and multiple other factors (eg.: readability, reliability) influence this direction of changes. 

## User point of view

From user point of view there will be no significant changes in the nearest future as it will be still possible to install Epiphany "classic way" so with single `epicli` configuration using whole codebase as monolith. 

For those who want to play with new features, or will need newly introduced possibilities, there will be short transition period which we consider as kind of "preview stage". In this period there will be need to run each module separately by hand in following order: 
 * moduleA init
 * moduleA plan
 * moduleA apply
 * moduleB init
 * moduleB plan
 * moduleB apply
 * ...
 
Init, plan and apply phases explanation you'll find in next sections of this document. Main point is that dependent modules have to be executed one after another during this what we called "preview stage". Later, with next releases there will be separate mechanism introduced to orchestrate modules dependencies and their consecutive execution. 

## New scenarios

In 0.8 we introduce possibility to use AKS or EKS as kubernetes providers. That is introduced with modules mechanism, so we introduced first four modules: 
 * [Azure Basic Infrastructure](https://github.com/epiphany-platform/m-azure-basic-infrastructure) (AzBI) module
 * [Azure AKS](https://github.com/epiphany-platform/m-azure-kubernetes-service) (AzKS) module
 * [AWS Basic Infrastructure](https://github.com/epiphany-platform/m-aws-basic-infrastructure) (AwsBI) module
 * [AWS EKS](https://github.com/epiphany-platform/m-aws-kubernetes-service) (AwsKS) module
 
Those 4 modules with the Classic Epiphany used with `any` provider allow change of on-prem kubernetes cluster with managed kubernetes services. 

As it might be already visible there are 2 paths provided: 
 * Azure related, using AzBI and AzKS modules, 
 * AWS related, using AwsBI and AwsKS modules. 
 
Those "... Basic Infrastructure" modules are responsible to provide basic cloud resources (eg.: resource groups, virtual networks, subnets, virtual machines, network security rules, routing, ect.) which will be used by next modules. So in this case, those are "... KS modules" meant to provide managed kubernetes services. They use some resources provided by basic infrastructure modules (eg.: subnets or resource groups) and instantiate managed kubernetes services provided by cloud providers. Last element in both those cloud provider related paths is Classic Epiphany installed on top of resources provided by those modules using `any` provider.    


