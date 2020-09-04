# PKI certificates management

## TLS certificates in a cluster

It's possible to regenerate kubernetes control plane certificates with epiphany.
To do so, additional configuration should be secified.

```yaml
kind: configuration/kubernetes-master
title: "Kubernetes Master Config"
name: default
provider: <provider>
specification:
  advanced:
    certificates:
      expiration_days: <int>
      renew: true
```

Parameters:

1. expiration_days - days to expire in, default value is `365`
2. renew - whether to renew certificates or not

## CA certificates rotation

This part cannot be done by epiphany. Refer to official [documentation](https://kubernetes.io/docs/tasks/tls/manual-rotation-of-ca-certificates/) to perform this task.

## References

1. [Best practices](https://kubernetes.io/docs/setup/best-practices/certificates/)
2. [Certificates management by kubeadm](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/)
3. [Kubernetes the hard way](https://github.com/kelseyhightower/kubernetes-the-hard-way/blob/master/docs/04-certificate-authority.md)
4. [Certificates generation with cfssl](https://gist.github.com/detiber/81b515df272f5911959e81e39137a8bb)
