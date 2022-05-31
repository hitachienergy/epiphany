## How to run epicli with temporary AWS credentials

There is a [possibility](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)
to generate temporary AWS credentials to manage resources.

To use this feature, first create temporary credentials:

```shell
aws sts get-session-token --duration-seconds <duration> --serial-number <mfa_serial_number> --token-code <mfa_token>
```

Then these credentials can be used in Epiphany config:

```yaml
kind: epiphany-cluster
title: Epiphany cluster Config
provider: aws
name: default
specification:
  cloud:
    credentials:
      access_key_id: <access_key_id>
      secret_access_key: <secret_access_key>
      session_token: <session_token>
```

## How to enable/disable Epiphany service user

There are a few ways to perform such task in Linux. To lock/unlock any user you can use the standard tools, such
as `usermod -l/-u`, `passwd --lock/--unlock`, `chage -E 0/-1`. Check `man` pages for more information.

Locking can also be done by changing the shell to `/sbin/nologin`, `/dev/null`, or `/bin/false` by manual editing of
`/etc/passwd` file or using `usermod` command:

```shell
usermod -s /sbin/nologin <user>
```

## How to add/remove additional users to/from OS

To add/remove users you need to provide additional section to `kind: epiphany-cluster` configuration.

You need to add `specification.users` in the format similar to example that you can find below:

```yaml
kind: epiphany-cluster
name: pg-aws-deb
provider: aws
specification:

  ...

  users:
    - name: user01 # name of the user
      sudo: true # does user have sudo privilege, not defined will set to false
      state: present # user will be added if not exist
      public_key: "ssh-rsa ..." # public key to add to .ssh/authorized_keys
    - name: user02
      state: absent # user will deleted if exists
      public_key: "ssh-rsa ..."
    - name: user03
      state: present
      public_key: "ssh-rsa ..."

  ...
```

## How to use TLS/SSL certificate with HA Proxy

HAProxy Load Balancer provides possibility to use TLS/SSL certificate to secure connection. This feature is called
HAProxy SSL Termination.

In basic configuration created by Epiphany SSL Termination is enabled by default:

```yaml
kind: configuration/haproxy
title: HAProxy
name: default
specification:
  frontend:
    - name: https_front
      port: 443
      https: true
      backend:
        - http_back1
```

Basic configuration uses ```test``` self-signed certificate generated during configuration.

To use other certificates than default copy ```*pem``` files inside ```files``` folder included into ```haproxy``` role.
In running ```epicli``` container absolute path is:

```bash
/usr/local/epicli/data/common/ansible/playbooks/roles/haproxy/files
```

Re-apply configuration will copy those files into location ```/etc/ssl/haproxy/``` and add appropriate configurations
into haproxy configuration file.

Default ```self_signed_*``` parameters visible in configuration files are ignored when user's certificates are placed
in ```haproxy/files``` location described above.

### TLS / SSL Parameters description:

| Parameter name | Default value | Description | | - | - | - | | self_signed_certificate_name |
self-signed-fullchain.pem | certificate name (ignored when user's cert in use) | | self_signed_private_key_name |
self-signed-privkey.pem | private key name (ignored when user's cert in use) | | self_signed_concatenated_cert_name |
self-signed-test.tld.pem |concatenated certificate name (ignored when user's cert in use) | | frontend / name |
https_front | frontend name (mandatory for every frontend) | | frontend / port | 443 | frontend binding port (mandatory,
must be unique across all machine) | | frontend / https | true | defines if https is used | | backend / name |
http_back1 | backend name (at least one is mandatory) | | backend / servers | kubernetes_node | list of backends (at
least one is mandatory) | | backend / port | 30104 | backend port (mandatory) | | backend / https | false | must be set
true if backend use https (will skip ssl verification between haproxy and backend) |

For more information about HA Proxy SSL Termination please check HA Proxy
blog [post](https://www.haproxy.com/blog/haproxy-ssl-termination/).

## How to use TLS/SSL with Kafka

Right now Epiphany supports only self-signed certificates generated and signed by CA self-sign certificate. If you want
to provide your own certificates, you need to configure Kafka manually according to Kafka documentation.

To use Epiphany automation and self-signed certificates you need to provide your own configuration for kafka role and
enable TLS/SSL as this is disabled by default.

To enable TLS/SSL communication in Kafka you can provide your own configuration of Kafka by adding it to your Epiphany
configuration file and set the `enabled` flag to `true` in the `security/ssl` section.

If in the `ssl` section you will also set the `parameter client_auth` parameter as `required`, you have to also provide
configuration of authorization and authentication as this setting enforces checking identity. This option is by default
set as
`required`. Values `requested` and `none` don't require such setup.

When TLS/SSL is turned on then all communication to Kafka is encrypted and no other option is enabled. If you need
different configuration, you need to configure Kafka manually.

When CA certificate and key is created on server it is also downloaded to host from which Epiphany was executed. By
default, Epiphany downloads this package to build output folder to `ansible/kafka_certs` directory. You can also change
this path in Epiphany configuration.

Sample configuration for Kafka with enabled TLS/SSL:

```yaml
kind: configuration/kafka
title: "Kafka"
name: default
specification:

  ...

  security:
    ssl:
      enabled: True
      port: 9093 # port on which Kafka will listen for encrypted communication
      server:
        local_cert_download_path: kafka-certs # path where generated key and certificate will be downloaded
        keystore_location: /var/private/ssl/kafka.server.keystore.jks # location of keystore on servers
        truststore_location: /var/private/ssl/kafka.server.truststore.jks # location of truststore on servers
        cert_validity: 365 # period of time when certificates are valid
        passwords: # in this section you can define passwords to keystore, truststore and key
          keystore: PasswordToChange
          truststore: PasswordToChange
          key: PasswordToChange

      endpoint_identification_algorithm: HTTPS # this parameter enforces validating of hostname in certificate
      client_auth: required # authentication mode for Kafka - options are: none (no authentication), requested (optional authentication), required (enforce authentication, you need to setup also authentication and authorization then)
    inter_broker_protocol: SSL # must be set to SSL if TLS/SSL is enabled

  ...
```

## How to use TLS/SSL certificates for Kafka authentication

To configure Kafka authentication with TLS/SSL, first you need to configure `ssl` section. Then you need to
add `authentication` section with `enabled` flag set to `true` and set `authentication_method`
as `certificates`. Setting `authentication_method` as `sasl` is not described right now in this document.

```yaml
kind: configuration/kafka
title: "Kafka"
name: default
specification:

  ...

  security:

    ...

    authentication:
      enabled: True
      authentication_method: certificates

  ...
```

## How to use TLS/SSL certificates for Kafka authorization

To configure Kafka authorization with TLS/SSL, first you need to configure `ssl` and `authentication` sections. If
authentication is disabled, then authorization will be disabled as well.

To enable authorization, you need to provide `authorization` section and set `enabled` flag to `True`.

For authorization, you can also provide different from default `authorizer_class_name`. By
default `kafka.security.auth.SimpleAclAuthorizer` is used.

If `allow_everyone_if_no_acl_found` parameter is set to `False`, Kafka will prevent accessing resources everyone except
super users and users having permissions granted to access topic.

You can also provide super users that will be added to Kafka configuration. To do this, you need to

- provide a list of users, like in the example below
- generate certificate on your own, only with CN that matches position that can be found in list

Do not set OU, DC or any other of parameters. Then the certificate needs to be signed by CA root certificate for Kafka.
CA root certificate will be downloaded automatically by Epiphany to location set
in `ssl.server.local_cert_download_path` or can be found on first Kafka host in `ssl.server.keystore_location`
directory. To access the certificate key, you need root privileges.

```yaml
kind: configuration/kafka
title: "Kafka"
name: default
specification:

  ...

  security:

    ...

    authorization:
      enabled: True
      authorizer_class_name: kafka.security.auth.SimpleAclAuthorizer
      allow_everyone_if_no_acl_found: False
      super_users:
        - tester01
        - tester02
  ...
```

## How to enable Azure disk encryption

Automatic encryption of storage on Azure is not yet supported by Epiphany. Guides to encrypt manually can be found:

- [Here](https://docs.microsoft.com/en-us/azure/security/fundamentals/azure-disk-encryption-vms-vmss) for VM storage.
- [Here](https://docs.microsoft.com/en-us/azure/storage/common/storage-service-encryption) for storage shares,

## How to use TLS/SSL certificate with RabbitMQ

To configure RabbitMQ TLS support in Epiphany you need to set `custom_configurations` in the configuration file and
manually create certificate with common CA according to documentation on your RabbitMQ machines:

https://www.rabbitmq.com/ssl.html#manual-certificate-generation

or:

https://www.rabbitmq.com/ssl.html#automated-certificate-generation

If `stop_service` parameter in `configuration/rabbitmq` is set to `true`, then RabbitMQ will be installed and stopped to
allow manual actions that are required to copy or generate TLS certificates.

---
**NOTE**

To complete installation it's required to execute `epicli apply` the second time with `stop_service` set to `false`

---

There is `custom_configurations` setting in Epiphany that extends RabbitMQ configuration with the custom one. Also, it
can be used to perform TLS configuration of RabbitMQ. To customize RabbitMQ configuration you need to pass a list of
parameters in format:

-name: rabbitmq.configuration.parameter value: rabbitmq.configuration.value

These settings are mapping to RabbitMQ TLS parameters configuration from documentation that you can find below the link:
https://www.rabbitmq.com/ssl.html

Below you can find example of TLS/SSL configuration.

```yaml

kind: configuration/rabbitmq
title: "RabbitMQ"
name: default
specification:

  ...

  custom_configurations:
    - name: listeners.tcp # option that disables non-TLS/SSL support
      value: none
    - name: listeners.ssl.default # port on which TLS/SSL RabbitMQ will be listening for connections
      value: 5671
    - name: ssl_options.cacertfile # file with certificate of CA which should sign all certificates
      value: /var/private/ssl/ca/ca_certificate.pem
    - name: ssl_options.certfile # file with certificate of the server that should be signed by CA
      value: /var/private/ssl/server/server_certificate.pem
    - name: ssl_options.keyfile # file with key to the certificate of the server
      value: /var/private/ssl/server/private_key.pem
    - name: ssl_options.password # password to key protecting server certificate
      value: PasswordToChange
    - name: ssl_options.verify # setting of peer verification
      value: verify_peer
    - name: ssl_options.fail_if_no_peer_cert # parameter that configure behaviour if peer cannot present a certificate
      value: "false"

  ...

```

Please be careful about boolean values as they need to be double-quoted and written in lowercase form. Otherwise,
RabbitMQ startup will fail.

## How to use TLS/SSL certificate with Kibana

For this moment it is not possible to automatically expose Kibana via https with using of Epiphany, but this can be
easily performed manually.

First, you need to generate certificate in .pem format.

After that, you need to change Kibana configuration file (```/etc/kibana/kibana.yml```) by adding and adjusting
following lines:

```yaml
server.ssl.enabled: true
server.ssl.certificate: /path_to_your_certificate.pem
server.ssl.key: /path_to_your_key.pem
```

To verify if the Kibana server is up and running you can use, for example, following command:

```bash
openssl s_client -connect your_ip:5601
```

## How to enable AWS disk encryption

### EC2 Root volumes

Encryption at rest for EC2 root volumes is turned on by default. To change this one can modify the `encrypted` flag for
the `root` disk inside a `infrastructure/virtual-machine` document:

```yaml
...
disks:
  root:
    volume_type: gp2
    volume_size: 30
    delete_on_termination: true
    encrypted: true
...
```

### Additional EC2 volumes

Encryption at rest for additional EC2 volumes is turned on by default. To change this one can modify the `encrypted`
flag for each `additional_disks` inside a `infrastructure/virtual-machine` document:

```yaml
...
disks:
  root:
  ...
  additional_disks:
    - device_name: "/dev/sdb"
      volume_type: gp2
      volume_size: 60
      delete_on_termination: true
      encrypted: true
...
```

### EFS storage

Encryption at rest for EFS storage is turned on by default. To change this one can modify the `encrypted` flag inside
the `infrastructure/efs-storage` document:

```yaml
kind: infrastructure/efs-storage
title: "Elastic File System Config"
provider: aws
name: default
specification:
  encrypted: true
...
```

Additional information can be found [here](https://docs.aws.amazon.com/efs/latest/ug/encryption-at-rest.html).

## How to use Kubernetes Secrets

Prerequisites: Epiphany Kubernetes cluster

1. SSH into the Kubernetes master.

2. Run `echo -n 'admin' > ./username.txt`, `echo -n 'VeryStrongPassword!!1' > ./password.txt`
   and  `kubectl create secret generic mysecret --from-file=./username.txt --from-file=./password.txt`

3. Copy over `secrets-sample.yaml` file from the example folder and run it with `kubectl apply -f secrets-sample.yaml`

4. Run `kubectl get pods`, copy the name of one of the ubuntu pods and run `kubectl exec -it POD_NAME -- /bin/bash` with
   it.

5. In the pods bash run `printenv | grep SECRET` - Kubernetes secret created in point 2 was attached to pods during
   creation (take a look at `secrets-sample.yaml`) and are available inside them as an environmental variables.

## How to authenticate to Azure AD app

1. Register you application. Go to Azure portal to `Azure Active Directory => App registrations` tab.

2. Click button `New application registration` fill the data and confirm.

3. Deploy app from [example](https://github.com/epiphany-platform/examples/tree/develop/dotnet/Epiphany.SampleApps/Epiphany.SampleApps.AuthService).

   This is a test service for verification Azure AD authentication of registered
   app.

4. Create secret key for your app `settings => keys`. Remember to copy value of key after creation.

5. Try to authenticate (e.g., using postman) calling service api `<service-url>/api/auth/` with following Body
   application/json type parameters :

    ```json
    {
      "TenantId": "<tenant-id>",
      "ClientId": "<client-id>",
      "Resource": "https://graph.windows.net/",
      "ClientSecret": "<client-secret>"
    }
    ```

- TenantId - Directory ID, which you find in `Azure active Directory => Properties` tab.

- ClientId - Application ID, which you find in details of previously registered
  app `Azure Active Directory => App registrations => your app`

- Resource - <https://graph.windows.net> is the service root of Azure AD Graph API. The Azure Active Directory (AD)
  Graph API provides programmatic access to Azure AD through OData REST API endpoints. You can construct your own Graph
  API
  URL. ([How to construct a Graph API URL](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-graph-api-quickstart))

- ClientSecret - Created secret key from 4. point.

6. The service should return Access Token.

## How to run epicli with password

Epiphany encrypts Kubernetes artifacts (access tokens) stored in Epiphany build directory. In order to achieve it, user
is asked for password which will be used for encryption and decryption of artifacts. Remember to enter the same password
for the same cluster - if password will not be the same, epicli will not be able to decrypt secrets.

Standard way of executing epicli has not been changed:

```shell
epicli apply -f demo.yaml
```

But you will be asked to enter a password:

```shell
Provide password to encrypt vault:
```

When running epicli from CI pipeline you can use new parameter for epicli:

```shell
epicli apply -f demo.yaml --vault-password MYPWD
```

## How to make kubectl work for non-root user on master node

For security reason, the access to the admin credentials is limited to the root user. To make a non-root user the
cluster administrator, run these commands (as the non-root user):

```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
