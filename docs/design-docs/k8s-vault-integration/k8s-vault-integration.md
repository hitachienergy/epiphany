# Epiphany Platform Kubernetes with Hashicorp Vault integration

Affected version: 0.7.x

## 1. Introduction

We want to provide integration of Kubernetes with Hashicorp Vault integration with couple of different modes:

1. vault - prod/dev mode without https
2. vault - prod/dev mode with https
3. vault - cluster with raft storage

We are not providing vault in vault development mode as this doesn't provide data persitency.

If user would like then can use automatic injecting of secrets into Kubernetes pods with usage of sidecar integration provided by
Hashicorp Vault agent. Sidecar will based on annotations for pods inject secrets as files to annotated pods.

## 2. Goal

In Epiphany Platform you can use Kubernetes secrets stored in etcd. We want to provide integration with Hashicorp Vault to provide
additional security for secrets used inside applications running in Epiphany Platform and also provide possibilty of usage safely
secrets for components that are running outside of Kubernetes cluster.

## 3. Design proposals

In all deployment models vault is installed outside Kubernetes cluster as a separate service. There is a possibility of usage
Hashicorp Vault deployed on Kubernetes cluster but this scenario is not covered in this document.

Integration between Kubernetes and Hashicorp Vault can be achieved via Hashicorp Vault Agent that is deployed on Kubernetes
cluster using Helm. Also to provide this Hashicorp Vault needs to be configured with proper policies and enabling kubernetes
method of authentication.

![Kubernetes Vault Integration](k8s-vault-integration.png)

In every mode we want to provide possibility to perform automatic unseal via script, but this solution is better suited for
development scenario. In production however to maximize security level unseal should be performed manually.

In all scenarios machine on which Hashicorp Vault will be running swap will be disabled and Hashicorp Vault will run under
user with limited privileges (e.g. vault). User under which Hashicorp Vault will be running will have ability to
use the mlock syscall In configuration from Epiphany side we want to provide possibility to turn off dumps at the system level
(turned off by default), use auditing (turned on by default) and disable root token after configuration (by default set to disable).

We want to provide three scenarios of installing Hashicorp Vault:

1. vault - prod/dev mode without https
2. vault - prod/dev mode with https
3. vault - cluster with raft storage

### 1. vault - prod/dev mode without https

In this scenario we want to use file storage for secrets.

### 2. vault - prod/dev mode with https

### 3. vault - cluster with raft storage

In this scenario we want to use raft storage for secrets.

## 4. Further extensions


