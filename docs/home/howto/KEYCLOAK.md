# Keycloak

## How to run Keycloak

1. Enable `kubernetes_master`, `kubernetes_node`, `repository` and `postgresql` components in the input manifest (yaml)
   by increasing `count` value. Enable `load_balancer` if needed.

    ```yaml
    kind: epiphany-cluster
    title: Epiphany cluster Config
    provider: azure
    name: default
    specification:
      components:
        repository:
          count: 1
        kubernetes_master:
          count: 1
        kubernetes_node:
          count: 2
        postgresql:
          count: 2
        load_balancer:
          count: 1
    ```

2. Enable `keycloak` in `configuration/features` doc:

    ```yaml
    kind: configuration/features
    title: Features to be enabled/disabled
    name: default
    specification:
      features:
        ...
        - name: keycloak
          enabled: true
    ```

3. Enable PostgreSQL related applications by setting `enabled: true` and adjust other parameters in `configuration/applications`
   doc.

    The default applications configuration is
    available [here](https://github.com/epiphany-platform/epiphany/blob/develop/schema/common/defaults/configuration/applications.yml)

    Note: To get working with Pgbouncer, Keycloak requires Pgbouncer configuration parameter `POOL_MODE` set to `session`,
    see [Installing Pgbouncer and Pgpool](DATABASES.md#installing-pgbouncer-and-pgpool) section. The reason is that Keycloak
    uses SET SQL statements. For details, see [SQL feature map for pooling modes](https://www.pgbouncer.org/features.html).

4. Adjust default Keycloak settings to your needs by editing `configuration/keycloak` doc.

    By default, only HTTPS protocol is enabled and auto-generated TLS certificate is used.

    You can provide your own certificate:

    ```yaml
    kind: configuration/keycloak
    title: Keycloak Config
    name: default
    specification:
      ...
      chart_values:
        secrets:
          ...
          tls-certs:
            type: kubernetes.io/tls
            data:
              # the data is abbreviated in this example
              # `ca.crt` is optional (not used by Keycloak)
              ca.crt: |
                LS0tLS1CRUdJTiBDRVJUSUZJQ0FUR...
              # a server certificate or certificate chain in PEM format
              tls.crt: |
                MIIC2DCCAcCgAwIBAgIBATANBgkqh...
              tls.key: |
                MIIEpgIBAAKCAQEA7yn3bRHQ5FHMQ...
    ```

    All default passwords should be changed. You may need to adjust `specification.chart_values.resources`.

    By default, Epiphany managed PostgreSQL cluster is used for Keycloak database
    and `specification.chart_values.database.hostname` is set to `AUTOCONFIGURED`
    which means: `pgbouncer` `ClusterIP` service is used if enabled, otherwise the first host of `postgresql` group.

5. Run `epicli apply` on your input manifest.

6. Reconfigure HA proxy (if needed).

    By default, Keycloak listens only for HTTPS traffic on port which is exposed via `NodePort` service.

    Some Keycloak features rely on the assumption that the remote address of the HTTP request connecting to Keycloak
    is the real IP address of the client machine.

    When you have HAProxy in front of Keycloak, this might not be the case, so we need to ensure that the X-Forwarded-For
    header is set by HAProxy. In order to achive this the content has to be modified by HAProxy. For that reason,
    TLS is terminated by HAProxy and the modified content is re-encrypted. Different keys and certificates are used on HAProxy
    as well as on Keycloak.

    Example of backend configuration:

    ```text
    backend keycloak
        balance roundrobin
        option forwardfor
        server kubernetes-node-vm-0 10.1.1.151:30104 check ssl verify required ca-file /etc/ssl/haproxy/epiphany-keycloak-ca.crt
        server kubernetes-node-vm-1 10.1.1.235:30104 check ssl verify required ca-file /etc/ssl/haproxy/epiphany-keycloak-ca.crt
    ```

    It's recommended to not expose some endpoints, see https://www.keycloak.org/server/reverseproxy#_exposed_path_recommendations.

    Example of frontend configuration:

    ```text
    frontend https_fe
        bind *:443 ssl crt /etc/ssl/haproxy/cert.crt
        # Do not expose health checks & metrics, see https://www.keycloak.org/server/reverseproxy#_exposed_path_recommendations
        http-request deny if { path_beg /auth/health/ } || { path /auth/health } || { path_beg /auth/metrics/ } || { path /auth/metrics }
        use_backend keycloak if { path -m beg /auth/ } || { path /auth }
    ```

7. Log into GUI

    Note: Accessing the Keycloak GUI depends on your configuration.

    One method for reaching GUI is to use SSH tunnel with forwarding `NodePort`:

    ```bash
    ssh -L 30104:localhost:30104 <user>@<k8s_host> -i <ssh_key_file>
    ```

    GUI should be reachable at: https://localhost:30104/auth
