# memory-stress-deployments

K8s deployments for generating memory load.

## Usage

1. Deploy deployments:

    ```bash
    kubectl apply -f memory-stress-deployments.yml
    ```

2. Get deployments:

    ```bash
    $ kubectl get deployment -l group=memory-stress
    NAME                              READY   UP-TO-DATE   AVAILABLE
    memory-stress-100m-no-request     0/0     0            0
    memory-stress-100m-with-request   0/0     0            0
    memory-stress-10m-no-request      0/0     0            0
    memory-stress-10m-with-request    0/0     0            0
    memory-stress-1g-no-request       0/0     0            0
    memory-stress-1g-with-request     0/0     0            0
    memory-stress-1m-no-request       0/0     0            0
    ```

3. Generate load by scaling up choosen deployments.

    The following example generates load of 1224 MB with resource requests:

    ```bash
    kubectl scale --replicas=1 deployment memory-stress-1g-with-request

    kubectl scale --replicas=2 deployment memory-stress-100m-with-request
    ```
