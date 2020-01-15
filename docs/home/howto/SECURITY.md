
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

## How to enable AWS disk encryption

### EC2 Root volumes

Since [May 2019](https://aws.amazon.com/about-aws/whats-new/2019/05/launch-encrypted-ebs-backed-ec2-instances-from-unencrypted-amis-in-a-single-step/) AWS supports the creation of instances from unencrypted AMIs. At this point Terraform does not [support](https://github.com/terraform-providers/terraform-provider-aws/issues/8624) this jet. If you need encrypted root volumes for now you need to supply your own pre-encryped AMIs as specified in the guide [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIEncryption.html).

We will add this as the functionality becomes available in Terraform. The issue is beeing tracked [here](https://github.com/epiphany-platform/epiphany/issues/381).

### Additional EC2 storage

When defining extra storage inside the `infrastructure/virtual-machine` document one can set the `encryption` flag:

```yaml
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

EFS storage is encrypted by default.

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
