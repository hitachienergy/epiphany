
## How to use TLS/SSL certificate with HA Proxy

TODO

## Azure disk encryption

TODO

## AWS disk encryption

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
