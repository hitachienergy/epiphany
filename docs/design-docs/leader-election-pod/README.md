## Leader election in Kubernetes

Components of control plane such as controller manager or scheduler use endpoints to select the leader. Instance which firstly create the endpoint of this service at the very beginning add annotation to the endpoint with the leader information.

Package `leaderelection.go` is used for leader election process which leverages above Kubernetes endpoint resource as some sort of `LOCK` primitive to prevent any follower to create the same endpoint in this same Namespace.

## Leader election for pods

As far as leader election for pods is considered there are possible a few solutions:

1. Since Kubernetes introduced in 1.14 version (March, 2019) `coordination.k8s.io` group API, it is possible to create in the cluster lease object which can hold the lock for the set of pods. It is necessary to implement a simple code into the application using package `leaderelection.go` in order to handle the leader election mechanism.

Helpful article:
- https://carlosbecker.com/posts/k8s-leader-election/

This is the recommended solution, simple, based on existing API group and lease object and not dependent on any external cloud object.

2. Kubernetes already uses Endpoints to represent a replicated set of pods so it is possible to use the same object for the purposes. It is possible to use already existing leader election framework from Kubernetes which implement simple mechanism. It is necessary to run leader-election container as sidecar container for replication set of application pods. Using the leader-election sidecar container, endpoint will be created which will be responsible for locking leader for one pod. Thanks to that, creating deployment with 3 pods, only one container with application will be in ready state - the one that works inside the pod leader. For application container, it is necessary to add readiness probe to the sidecar container:

Helpful article:
- https://kubernetes.io/blog/2016/01/simple-leader-election-with-kubernetes/

This solution was recommended by Kubernetes in 2016 and looks a little bit outdated, is complex and require some work.

3. Microsoft and Google come up with a proposal to use cloud native storage with single object that contain the leader data but it requires to read that file by each node what can be in some situations problematic.

Helpful articles:
- https://cloud.google.com/blog/topics/developers-practitioners/implementing-leader-election-google-cloud-storage
- https://docs.microsoft.com/en-us/azure/architecture/patterns/leader-election

It is not recommended solution since the single object is a potential single point of failure.
