# Epiphany Platform Autoscaling

Affected version: 0.7.x

## 1. Goals

We want to provide automatic scale up / down feature for cloud-based Epiphany clusters (currently Azure and AWS).

- Clusters will be resized in reaction to the resource utilisation (CPU and Memory).
- Existing Epiphany automation will be reused and optimized for the purpose of autoscaling.
- Additional nodes will be added (removed) to (from) running Kubernetes clusters.
- [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) will be used to control number of pods for particular deployment.

## 2. Design proposal

### PHASE 1: Adding ability to scale-down the pool of worker nodes.

- Current Epiphany codebase does not allow to scale-down Kubernetes clusters in the nice / proper way.
- This is crucial for autoscaling to work, as we need to properly drain and delete physically-destroyed nodes from Kuberentes.
- Also this step needs to be performed before terraform code is executed (which requires a refactor of epicli code).

### PHASE 2: Moving terraform's state and epiphany-cluster-config to a shared place in the cloud.

- Currently Epiphany keeps state files and cluster configs in the `build/xxx/` directories, which causes them not to be shared easily.
- To solve the issue, terraform beckends can be used: [for Azure](https://www.terraform.io/docs/backends/types/azurerm.html) and [for AWS](https://www.terraform.io/docs/backends/types/s3.html).
- For simplicity the same "bucket" can be used to store and share epiphany-cluster-config.

### PHASE 3: Building packer images to quickly add new Kubernetes nodes.

- Autoscaling is expected to react reasonably quickly. Providing pre-built images should result in great speed-ups.
- Packer code should be added to the epicli codebase somewhere "before" the terraform code executes.

### PHASE 4: Realistic provisioning minimalization and speedup.

- Currently Epiphany's automation takes lots of time to provision clusters.
- [Limits](https://docs.ansible.com/ansible/latest/user_guide/intro_patterns.html#patterns-and-ansible-playbook-flags) and [tags](https://docs.ansible.com/ansible/latest/user_guide/playbooks_tags.html) can be used to filter-out unnecessary plays from ansible execution (for now, narrowing it just to the Kubernetes node provisioning).

### PHASE 5: Adding ability to authenticate and run epicli from a pod.

- To be able to execute epicli form a running Epiphany cluster, it is required to deploy SSH keys and cloud access configuration (ie. Service Principal).
- SSH keys can be created and distributed automatically (in Ansible) just for the purpose of autoscaling.
- For now, it seems resonable to store them in Kubernetes secrets (later the Hashicorp Vault will be used).

### PHASE 6: Introducing python application that will execute epicli from a pod (in reaction to performance metrics) to scale the pool of worker nodes.

- Metrics can be obtained from the [metrics server](https://github.com/kubernetes-sigs/metrics-server).
- For simplicity, standard CPU / Memory metrics will be used, but later it should be posible to introduce [custom metrics](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-custom-metrics) taken from Prometheus.
- Best way to package and deploy the application would be to use Helm (v3).
- The docker image for the application can be stored in a public docker registry.

### PHASE 7: Introducing standard Horizontal Pod Autoscaler to scale pods in Epiphany clusters.

- To scale Kubernetes pods in Epiphany clusters the [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/) will be used.
- This step will be dependent and the user / customer (user will deploy and configure proper resources inside Kubernetes).

[//]: # ( vim:set ts=2 sw=2 et syn=markdown: )
