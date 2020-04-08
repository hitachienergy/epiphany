# Epiphany Platform Kubernetes with Hashicorp Vault integration without sidecar - development purpose

Affected version: 0.7.x

## 1. Introduction

To start integration of Kubernetes with Hashicorp Vault easiest way is to introduce first vault development setup with vault agent
and Kubernetes, which can give us additional input from users. The next steps will require introducing sidecar integration with
automatic injecting of secrets into Kubernetes and after that cluster setup of Hashicorp vault for production use.

## 2. Goal

In Epiphany Platform you can use Kubernetes secrets stored in etcd. We want to provide integration with Hashicorp Vault to provide
additional security for secrets used inside applications running in Epiphany Platform.

## 3. Design proposal

Basic setup of Hashicorp Vault will require only to install Hashicorp Vault and enabling kubernetes method of authentication. This 
will use Kubernetes Service Account Token to provide authentication for Pods which let to automatically
authenticate with Vault and retrieve a client token via Vault Agent().