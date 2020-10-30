# PKI certificates management

## TLS certificates in a cluster

It's possible to regenerate Kubernetes control plane certificates with Epiphany.
To do so, additional configuration should be specified.

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

Parameters (optional):

1. expiration_days - days to expire in, default value is `365`
2. renew - whether to renew certificates or not, default value is `false`

---
**NOTE**

Usage of values greater than 24855 for `expiration_days` is not possible.
For more information see [discussion](https://groups.google.com/g/mailing.openssl.users/c/3kK_f0ywCZQ) about that.

---

When `epicly apply` executes, if `renew` option is set to `true`, following certificates will be renewed with expiration period defined by `expiration_days`:

1. admin.conf
2. apiserver
3. apiserver-etcd-client
4. apiserver-kubelet-client
5. controller-manager.conf
6. etcd-healthcheck-client
7. etcd-peer
8. etcd-server
9. front-proxy-client
10. scheduler.conf

---
**NOTE**

kubelet.conf is not renewed because kubelet is configured for automatic certificate renewal.
To verify that, navigate to `/var/lib/kubelet/` and check `config.yaml` file, where `rotateCertificates` setting is `true` by default.

---

## CA certificates rotation

This part cannot be done by Epiphany. Refer to official Kubernetes [documentation](https://kubernetes.io/docs/tasks/tls/manual-rotation-of-ca-certificates/) to perform this task.

## References

1. [Best practices](https://kubernetes.io/docs/setup/best-practices/certificates/)
2. [Certificates management by kubeadm](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/)
3. [Kubernetes the hard way](https://github.com/kelseyhightower/kubernetes-the-hard-way/blob/master/docs/04-certificate-authority.md)
4. [Certificates generation with cfssl](https://gist.github.com/detiber/81b515df272f5911959e81e39137a8bb)
