## How to enable/disable Epiphany service user

To enable/disable Epiphany service user you can use tool from our repository. You can find this in directory `tools/service_user_disable_enable` under name `service-user-disable-enable.yml`.

To use this you need to have Ansible installed on machine from which you want to execute this.

To disable user you need to run command:

```sh
ansible-playbook -i inventory --extra-vars "operation=disable name=your_service_user_name" service-user-disable-enable.yml
```

To enable user you need to run command:

```sh
ansible-playbook -i inventory --extra-vars "operation=enable name=your_service_user_name" service-user-disable-enable.yml
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
      sudo: true # does user have sudo priviledge, not defined will set to false
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

TODO

## How to use TLS/SSL with Kafka

Right now Epiphany supports only self-signed certificates 
generated and signed by CA self-sign certificate. If you want to 
provide your own certificates you need to configure Kafka 
manually according to Kafka documentation.

To use Epiphany automation and self-signed certificates you need 
to provide your own configuration for kafka role and enable TLS/SSL 
as this is disabled by default.

To enable TLS/SSL communication in Kafka you can provide your own 
configuration of Kafka by adding it to your Epiphany configuration file
and set the `enabled` flag to `true` in the `security/ssl` section.

If in the `ssl` section you will also set the `parameter client_auth` parameter as `required`,
you have to also provide configuration of authorization and authentication
as this setting enforces checking identity. This option is by default set as 
`required`. Values `requested` and `none` don't require such setup.

When TLS/SSL is turned on then all communication to Kafka is encrypted and no
other option is enabled. If you need different configuration, you need to configure
Kafka manually.

When CA certificate and key is created on server it is also downloaded to host from 
which Epiphany was executed. By default Epiphany downloads this package to build output 
folder to `ansible/kafka_certs` directory. You can also change this path in Epiphany configuration.

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

To configure Kafka authentication with TLS/SSL, first you need to configure `ssl` section.
Then you need to add `authentication` section with `enabled` flag set to `true` and set `authentication_method`
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

To configure Kafka authorization with TLS/SSL, first you need to configure `ssl` and `authentication` sections.
If authentication is disabled, then authorization will be disabled as well.

To enable authorization, you need to provide `authorization` section and set `enabled` flag to `True`.

For authorization you can also provide different than default `authorizer_class_name`.
By default `kafka.security.auth.SimpleAclAuthorizer` is used.

If `allow_everyone_if_no_acl_found` parameter is set to `False`, Kafka will prevent accessing resources everyone
except super users and users having permissions granted to access topic.

You can also provide super users that will be added to Kafka configuration. To do this you need to provide list of users,
like in the example below, and generate certificate on your own only with CN that matches position that can be found in list 
(do not set OU, DC or any other of parameters). Then the certificate needs to be signed by CA root certificate for Kafka.
CA root certificate will be downloaded automatically by Epiphany to location set in `ssl.server.local_cert_download_path` or can be found on first Kafka host in `ssl.server.keystore_location` directory. To access the certificate key, you need root priviledges.

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

To configure RabbitMQ SSL/TLS support in Epiphany you need to set `custom_configurations` in Epiphany configuration file and you need to 
manually create certificate with common CA according to documentation on your RabbitMQ machines: 

https://www.rabbitmq.com/ssl.html#manual-certificate-generation

or:

https://www.rabbitmq.com/ssl.html#automated-certificate-generation

If in `custom_configurations` parameter `listeners.ssl.default` is set then RabbitMQ will be installed and stopped to allow you to perform manual actions required to create server certificates with CA certificate.

`custom_configurations` are settings in Epiphany, that are to extend RabbitMQ configuration with your custom one. We can also use this to 
perform TLS configuration of RabbitMQ. To add custom configuration to RabbitMQ configuration you need to pass list of attributes in format:

-name: rabbitmq.configuration.parameter
 value: rabbitmq.configuration.value

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

Right now RabbitMQ configuration is available only for standalone machines. Also please be carreful about boolean values as they need to be double quoted 
and written in lowercase form as this will RabbitMQ startup fail.

## How to enable AWS disk encryption

### EC2 Root volumes

Encryption at rest for EC2 root volumes is turned on by default. To change this one can modify the `encrypted` flag for the `root` disk inside a `infrastructure/virtual-machine` document:

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

Encryption at rest for additional EC2 volumes is turned on by default. To change this one can modify the `encrypted` flag for each `additional_disks` inside a `infrastructure/virtual-machine` document:

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

Encryption at rest for EFS storage is turned on by default. To change this one can modify the `encrypted` flag inside the `infrastructure/efs-storage` document:

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

2. Run `echo -n 'admin' > ./username.txt`, `echo -n 'VeryStrongPassword!!1' > ./password.txt` and  `kubectl create secret generic mysecret --from-file=./username.txt --from-file=./password.txt`

3. Copy over `secrets-sample.yaml` file from the example folder and run it with `kubectl apply -f secrets-sample.yaml`

4. Run `kubectl get pods`, copy the name of one of the ubuntu pods and run `kubectl exec -it POD_NAME -- /bin/bash` with it.

5. In the pods bash run `printenv | grep SECRET` - Kubernetes secret created in point 2 was attached to pods during creation (take a look at `secrets-sample.yaml`) and are availiable inside of them as an environmental variables.

## How to authenticate to Azure AD app

1. Register you application. Go to Azure portal to `Azure Active Directory => App registrations` tab.

2. Click button `New application registration` fill the data and confirm.

3. Deploy app from `examples/dotnet/Epiphany.SampleApps/Epiphany.SampleApps.AuthService`.

    This is a test service for verification Azure AD authentication of registered app. ([How to deploy app](#how-to-run-an-example-app))

4. Create secret key for your app `settings => keys`. Remember to copy value of key after creation.

5. Try to authenticate (e.g. using postman) calling service api `<service-url>/api/auth/` with following Body application/json type parameters :

    ```json
    {
      "TenantId": "<tenant-id>",
      "ClientId": "<client-id>",
      "Resource": "https://graph.windows.net/",
      "ClientSecret": "<client-secret>"
    }
    ```

    - TenantId - Directory ID, which you find in `Azure active Directory => Properties` tab.

    - ClientId - Application ID, which you find in details of previously registered app `Azure Active Directory => App registrations => your app`

    - Resource - <https://graph.windows.net> is the service root of Azure AD Graph API. The Azure Active Directory (AD) Graph API provides programmatic access to Azure AD through OData REST API endpoints. You can construct your own Graph API URL. ([How to construct a Graph API URL](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-graph-api-quickstart))

    - ClientSecret - Created secret key from 4. point.

6. The service should return Access Token.

## How to run epicli with password

Epiphany encrypts Kubernetes artifacts (access tokens) stored in Epiphany build directory. In order to achieve it, user is asked for password which will be used for encryption and decryption of artifacts. Remember to enter the same password for the same cluster - if password will not be the same, epicli will not be able to decrypt secrets.

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

## How to enable kubectl on Kubernetes master

For security reasons kubectl is disabled by default on the Kubernetes master node. To enable it execute the following commands:

```shell
cp /etc/kubernetes/admin.conf $HOME/
chown $(id -u):$(id -g) $HOME/admin.conf
export KUBECONFIG=$HOME/admin.conf
```

## How to turn on Hashicorp Vault functionality

In Epiphany beside storing secrets in Kubernetes Secrets there is also a possibility of using Vault from Hashicorp. This can provide much more sophisticated solution for using secrets and also higher level of security than standard Kubernetes implementation. Also Epiphany provides transparent method to access Hashicorp Vault secrets with applications running on top of Kubernetes, about what you can read in the [How to turn on Hashicorp Vault integration with k8s](./SECURITY.md#how-to-turn-on-hashicorp-vault-integration-with-k8s) section. In the future we want also to provide additional features that right now can be configured manually according to Hashicorp Vault [configuration](https://www.vaultproject.io/docs). Right now only installation on Kubernetes Master is provided, but we are also planning separate installation with no other components. 

Below you can find sample configuration for Vault with description of all options.

```yaml
kind: configuration/vault
title: Vault Config
name: default
specification:
  vault_enabled: true # this setting needs to be provide to install Vault
  vault_system_user: vault # this is name of user under which Vault service will be running
  vault_system_group: vault # this is name of group under which Vault service will be running
  enable_vault_audit_logs: false # this is an option to turn on audit logs that can be found at /opt/vault/logs/vault_audit.log
  enable_vault_ui: false # this is an
  vault_script_autounseal: true # this is an option to automatically unseal vault at the start of the service, shouldn't be used at production
  vault_script_autoconfiguration: true # this is option to perform automatic configuration of Hashicorp Vault
  tls_disable: false
  ...
  app_secret_path: devwebapp
  revoke_root_token: false # not implemented yet
  secret_mount_path: secret
  vault_token_cleanup: true
  vault_install_dir: /opt/vault
  vault_log_level: info
  certificate_name: fullchain.pem
  private_key_name: privkey.pem
  vault_tls_valid_days: 365
  override_existing_vault_users: false # 
  vault_users: # users that will be 
    - name: admin
      policy: admin
    - name: provisioner
      policy: provisioner
```

[policies](https://www.hashicorp.com/resources/policies-vault/)

### Configuration with manual unsealing

### Creating your own policy

### Creating your own user

### Root token revocation

### Troubleshooting

To perform troubleshooting of vault and find the root cause of the problem please enable 


## How to turn on Hashicorp Vault integration with k8s

In Epiphany there is also an option to configure automatically integration with Kubernetes. This is achieved with usage of 

```yaml
kind: configuration/vault
title: Vault Config
name: default
specification:
  vault_enabled: true
  vault_system_user: vault
  vault_system_group: vault
  ...
  vault_script_autounseal: true
  vault_script_autoconfiguration: true
  ...
  kubernetes_integration: true
  kubernetes_configuration: true
  enable_vault_kubernetes_authentication: true
  kubernetes_namespace: default
  ...
```





```shell
vault kv put secret/yourpath/to/secret username='some_user' password='some_password'
```

```yaml
  template:
    metadata:
      labels:
        app: devwebapp
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "devweb-app"
        vault.hashicorp.com/agent-inject-secret-credentials.txt: "secret/data/yourpath/to/secret"
        vault.hashicorp.com/tls-skip-verify: "true"
```

[annotations](https://www.vaultproject.io/docs/platform/k8s/injector/annotations).

