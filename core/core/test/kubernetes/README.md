# Kubernetes Cluster Testing

## Scripts

<!-- TOC -->

- [Install Prerequisites](#prerequisites-installation)
- [Run Tests](#test-run)
   
<!-- /TOC -->

## Install prerequisites - install-test-prerequisites.sh

Testing conformance of Kubernetes cluster installation is done using sonobuoy plugins: https://github.com/heptio/sonobuoy. Sonobuoy plugin is golang package and requires golang installation. Script will install golang and set environment variables for golang binaries and plugins path. 

## Run Tests - run-sonobuoy-test.sh

Script will execute conformance tests for Kubernetes cluster. Go to [run-sonobuoy-test script](run-sonobuoy-test.sh) to see prerequisites of that tool. 

Sonobuoy tests once launched, will work in background and the only way to know te the status of it's work is to call `sonobuoy status`. Script will wait till status command will return complete flag.

