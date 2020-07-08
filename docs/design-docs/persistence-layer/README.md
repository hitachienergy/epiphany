# Intent

This document aim is to initialize evaluation of possible persistence layers for Kubernetes cluster (a.k.a. Cloud Native Storage, CNS) in various setups. 

# Conditions

There is need to provide persistence layer for Kubernetes cluster installed as Epiphany containers orchestrator. We need to consider performance of persistence layer as well. There is possibility to utilize external persistence solutions in future with managed Kubernetes clusters installations, but that is out of scope of this document.  

# OKR

This section proposes Objectives and Key Results for CNS.

1. O1: Introduce Cloud Native Storage
   1. O1KR1: Have stable CNS released
   2. O1KR2: Have CNS performance tests automation
   3. O1KR3: Have CNS performance tests results

# Possible solutions
As for now I can see following solutions: 
-	Ceph managed by Rook Operator
-	GlusterFS (managed by Heketi or Kadalu, but that would need further assessment)

We should review more solutions presented [here](https://landscape.cncf.io/category=cloud-native-storage&format=card-mode&license=open-source). 

There are numerous other solutions possible to use over CSI, but they require separate management. 

# Requirements
- It has to be able to work on-premise
- It has to be able to work offline
- There need to be known difference in performance of middleware components
- Storage layer should be tightly integrated with Kubernetes 
- As much as possible automation is required (zero-management)

# Tests
- We need to have performance tests automated
- Tests have to be executed daily
- We should have PostgreSQL database performance tests automated
- We should have kafka performance tests automated

# Initial Plan
1. Have epiphany cluster with PostgreSQL database
2. Create performance test running in Kubernetes pod using PostgreSQL in current setup (pgbench can be used) 
3. Deploy rook operator and create Ceph cluster
4. Create PostgreSQL database running in Kubernetes pod using Ceph PVC
5. Run performance test using Kubernetes PostgreSQL instance
6. Compare results
