#!/bin/bash

echo "==== All Kubernetes worker nodes will be deleted ===="

worker_nodes=$(kubectl get nodes --selector='!node-role.kubernetes.io/control-plane' -o jsonpath='{.items[*].metadata.name}')

for node in $worker_nodes; do
    echo "> Deleting $node node."
    kubectl delete node $node
done

echo "==== Kubernetes nodes deletion completed ===="
