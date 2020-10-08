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

## How to make kubectl work for non-root user on master node

For security reason, the access to the admin credentials is limited to the root user.
To make a non-root user the cluster administrator, run these commands (as the non-root user):

```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## How to turn on Hashicorp Vault functionality

In Epiphany beside storing secrets in Kubernetes secrets there is also a possibility of using secrets stored in Vault
from Hashicorp. This can provide much more sophisticated solution for using secrets and also higher level of security
than standard Kubernetes secrets implementation. Also Epiphany provides transparent method to access Hashicorp Vault
secrets with applications running on Kubernetes. You can read in the more about it in [How to turn on Hashicorp Vault integration with k8s](./SECURITY.md#how-to-turn-on-hashicorp-vault-integration-with-k8s) section. In the future we want also to provide additional features
that right now can be configured manually according to Hashicorp Vault [documentation](https://www.vaultproject.io/docs).

At the moment only installation on Kubernetes Master is supported, but we are also planning separate installation with no
other components. Also at this moment we are not providing clustered option for Vault deployment, but this will be part
of the future releases. For multi-master (HA) Kubernetes, Vault is not installed.

Below you can find sample configuration for Vault with description of all options.

```yaml
kind: configuration/vault
title: Vault Config
name: default
specification:
  vault_enabled: true # enable Vault install
  vault_system_user: vault # user name under which Vault service will be running
  vault_system_group: vault # group name under which Vault service will be running
  enable_vault_audit_logs: false # turn on audit logs that can be found at /opt/vault/logs/vault_audit.log
  enable_vault_ui: false # enable Vault UI, shouldn't be used at production
  vault_script_autounseal: true # enable automatic unseal vault at the start of the service, shouldn't be used at production
  vault_script_autoconfiguration: true # enable automatic configuration of Hashicorp Vault. It sets the UNSEAL_VAULT variable in script.config
  ...
  app_secret_path: devwebapp # application specific path where application secrets will be mounted
  revoke_root_token: false # not implemented yet (more about in section Root token revocation)
  secret_mount_path: secret # start of the path that where secrets will be mounted
  vault_token_cleanup: true # should configuration script clean token
  vault_install_dir: /opt/vault # directory where vault will be installed
  vault_log_level: info # logging level that will be set for Vault service
  override_existing_vault_users: false # should user from vault_users ovverride existing user and generate new password
  vault_users: # users that will be created with vault
    - name: admin # name of the user that will be created in Vault
      policy: admin # name of the policy that will be assigned to user (descrption bellow)
    - name: provisioner
      policy: provisioner
  vault_helm_chart_values: # helm chart values overwriting the default package (to be able to use internal registry for offline purposes)
    injector:
      externalVaultAddr: https://your-external-address:8200 # external vault address (only if you want to setup address to provide full name to use with signed certificate) [IMPORTANT: switch https->http if tls_disable parameter is set to true]
      image:
        repository: "{{ image_registry_address }}/hashicorp/vault-k8s" # docker image used by vault injector in kubernetes
      agentImage:
        repository: "{{ image_registry_address }}/vault" # docker image used by vault injector in kubernetes
    server:
      image:
        repository: "{{ image_registry_address }}/vault" # docker image used by vault injector in kubernetes
  # TLS part
  tls_disable: false # enable TLS support, should be used always in production
  certificate_name: fullchain.pem # certificate file name
  private_key_name: privkey.pem # private key file name for certificate
  vault_tls_valid_days: 365 # certificate valid time in days
  selfsigned_certificate: # selfsigned certificate information
    country: US # selfexplanatory
    state: state # selfexplanatory
    city: city # selfexplanatory
    company: company # selfexplanatory
    common_name: "*" # selfexplanatory

```

More information about configuration of Vault in Epiphany and some guidance how to start working with Vault with Epiphany you can find below.

To get more familiarity with Vault usage you can reffer to [official getting started](https://learn.hashicorp.com/vault) guide.

### Creation of user using Epiphany in Vault

To create user by Epiphany please provide list of users with name of policy that should be assigned to user. You can
use predefined policy delivered by Epiphany, default Vault policies or your own policy. Remember that if you have
written your own policy it must exist before user creation.

Password for user will be generated automatically and can be found in directory /opt/vault in files matching
tokens-*.csv pattern. If user password will be generated or changed you will see corresponding line in csv file with
username, policy and password. If password won't be updated you will see `ALREADY_EXISTS` in password place.

### Predefined Vault policies

Vault policies are used to define Role-Based Access Control that can be assigned to clients, applications and other
components that are using Vault. You can find more information about policies [here](https://www.hashicorp.com/resources/policies-vault/).

Epiphany besides two already included in vault policies (root and default) provides two additional predefined policies:

- admin - policy granting administration privileges, have sudo permission on Vault system endpoints
- provisioner - policy granting permissions to create user secrets, adding secrets, enable authentication methods, but
  without access to Vault system endpoints

### Manual unsealing of the Vault

By design Hashicorp Vault starts in sealed mode. It means that Vault data is encrypted and operator needs to provide unsealing key to be able to access data.

Vault can be unsealed manually using command:

```bash
vault operator unseal
```

and passing three unseal keys from /opt/vault/init.txt file. 
Number of keys will be defined from the level of Epiphany configuration in the future releases.
Right now we are using default Hashicorp Vault settings.

For development purposes you can also use `vault_script_autounseal` option in Epiphany configuration.

More information about unseal you can find in documentation for [CLI](https://www.vaultproject.io/docs/commands/operator/unseal)
and about concepts [here](https://www.vaultproject.io/docs/concepts/seal).

### Configuration with manual unsealing

If you are using option with manual unseal or want to perform manual configuration you can run script later on manually
from the command line:

```bash
/opt/vault/bin/configure-vault.sh
        -c /opt/vault/script.config
        -a ip_address_of_vault
        -p http | https
        -v helm_chart_values_be_override
```

Values for script configuration in script.config are automatically generated by Epiphany and can be later on used to
perform configuration.

### Log into Vault with token

To log into Vault with token you just need to pass token. You can do this using command:

```bash
vault login
```

Only root token has no expiration date, so be aware that all other tokens can expire. To avoid such situations you need
to renew the token. You can assign policy to token to define access.

More information about login with tokens you can find [here](https://www.vaultproject.io/docs/commands/login) and about
tokens [here](https://www.vaultproject.io/docs/concepts/tokens).

### Log into Vault with user and password

Other option to log into Vault is to use user/password pair. This method doesn't have disadvantage of login each time
with different token after expire. To login with user/password pair you need to have userpass method and login with command:

```bash
vault login -method=userpass username=your-username
```

More information about login with tokens you can find [here](https://www.vaultproject.io/docs/commands/login) and about
userpass authentication [here](https://www.vaultproject.io/docs/auth/userpass).

### Token Helpers

Vault provide option to use token helper. By default Vault is creating a file .vault-token in home directory of user
running command vault login, which let to user perform automatically commands without providing a token. This token
will be removed by default after Epiphany configuration, but this can be changed using `vault_token_cleanup flag`.

More information about token helper you can find [here](https://www.vaultproject.io/docs/commands/token-helper).

### Creating your own policy

In order to create your own policy using CLI please refer to [CLI documentation](https://www.vaultproject.io/docs/commands)
and [documentation](https://www.vaultproject.io/docs/concepts/policies).

### Creating your own user

In order to create your own user with user and password login please refer to [documentation](https://www.vaultproject.io/docs/auth/userpass).
If you have configured any user using Epiphany authentication userpass will be enabled, if not needs to be enabled manually.

### Root token revocation

In production is a good practice to [revoke root token](https://www.vaultproject.io/docs/commands/token/revoke). This option is not implemented yet,
by Epiphany, but will be implemented in the future releases.

Be aware that after revoking root token you won't be able to use configuration script without generating new token
and replace old token with the new one in /opt/vault/init.txt (field `Initial Root Token`). For new root token generation
please refer to documentation accessible [here](https://learn.hashicorp.com/vault/operations/ops-generate-root).

### TLS support

By default tls_disable is set to false which means that certificates are used by vault. There are 2 ways of certificate configuration:

1. selfsigned

Vault selfsigned certificates are generated automatically during vault setup if no custom certificates are present in dedicated location.

2. certificate provided by user

In dedicated location user can add certificate (and private key). File names are important and have to be the same as provided in configuration and ```.pem``` file extensions are required.

Dedicated location of custom certificates:
```core/src/epicli/data/common/ansible/playbooks/roles/vault/files/tls-certs```

Certificate files names configuration:

```yaml
kind: configuration/vault
title: Vault Config
name: default
specification:
...
  certificate_name: fullchain.pem # certificate file name
  private_key_name: privkey.pem # private key file name for certificate
...
```

### Production hardening for Vault

In Epiphany we have performed a lot of things to improve Vault security, e.g.:

- End-to-End TLS
- Disable Swap (when running on Kubernetes machine)
- Don't Run as Root
- Turn Off Core
- Enable Auditing
- Restrict Storage Access
- Tweak ulimits

However if you want to provide more security please refer to this
[guide](https://learn.hashicorp.com/vault/operations/production-hardening).

### Troubleshooting

To perform troubleshooting of vault and find the root cause of the problem please enable audit logs and set vault_log_level
to debug. Please be aware that audit logs can contain sensitive data.

## How to turn on Hashicorp Vault integration with k8s

In Epiphany there is also an option to configure automatically integration with Kubernetes. This is achieved
with applying additional settings to Vault configuration. Sample config with description you can find below.

```yaml
kind: configuration/vault
title: Vault Config
name: default
specification:
  vault_enabled: true
  ...
  vault_script_autounseal: true
  vault_script_autoconfiguration: true
  ...
  kubernetes_integration: true # enable setup kubernetes integration on vault side
  kubernetes_configuration: true # enable setup kubernetes integration on vault side
  enable_vault_kubernetes_authentication: true # enable kubernetes authentication on vault side
  kubernetes_namespace: default # namespace where your application will be deployed
  ...
```

Vault and Kubernetes integration in Epiphany relies on vault-k8s tool.
Thit tool enables sidecar injection of secret into pod with usage of Kubernetes Mutating Admission Webhook. This is transparent
for your application and you do not need to perform any binding to Hashicorp libaries to use secret stored in Vault.

You can also configure Vault manually on your own enabling by Epiphany only options that are necessary for you.

More about Kubernetes sidecar integration you can find at the [link](https://www.hashicorp.com/blog/injecting-vault-secrets-into-kubernetes-pods-via-a-sidecar/).

### Vault Kubernetes authentication

To work with sidecar integration with Vault you need to enable Kubernetes authentication. Without that sidecar won't be able
to access secret stored in Vault.

If you don't want to use sidecar integration, but you want to access automatically Vault secrets you can use Kubernetes
authentication. To find more information about capabilities of Kubernetes authentication please refer to [documentation](https://www.vaultproject.io/docs/auth/kubernetes).

### Create your secret in Vault

In Epiphany you can use integration of key value secrets to inject them into container. To do this you need to create them
using vault CLI.

You can do this running command similar to sample below:

```shell
vault kv put secret/yourpath/to/secret username='some_user' password='some_password'
```

Epiphany as backend for Vault secrets is using kv secrets engine. More information about kv secrets engine you can find
[here](https://www.vaultproject.io/docs/secrets/kv).

### Kubernetes namespace

In Epiphany we are creating additional Kubernetes objects to inject secrets automatically using sidecar. Those objects
to have access to your application pods needs to be deployed in the same namespace.

### Annotations

Below you can find sample of deployment configuration excerpt with annotations. For this moment `vault.hashicorp.com/role`
cannot be changed, but this will change in future release.

```yaml
  template:
    metadata:
      labels:
        app: yourapp
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "devweb-app"
        vault.hashicorp.com/agent-inject-secret-credentials.txt: "secret/data/yourpath/to/secret"
        vault.hashicorp.com/tls-skip-verify: "true"
```

```vault.hashicorp.com/tls-skip-verify```
If true, configures the Vault Agent to skip verification of Vault's TLS certificate. 
It's mandatory for selfsigned certificates and not recommended to set this value to true in a production environment.

More information about annotations you can find [here](https://www.vaultproject.io/docs/platform/k8s/injector/annotations).
