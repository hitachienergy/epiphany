# KeyCloak examples readme

## Contents

- [Introduction](#introduction)
- [Security concerns](#security-concerns)
- [Prerequisites](#prerequisites)
- [Setup test instance of KeyCloak](#setup-test-instance-of-KeyCloak)
- [Implicit flow examples](#implicit-flow-examples)
  - [Implicit ReactJS SPA](#implicit-reactjs-spa)
  - [Implicit Python](#implicit-python)
  - [Implicit .NET Core](#implicit-.net-core)
  - [Implicit Java](#implicit-java)
- [Authorization flow examples](#authorization-flow-examples)
  - [Authorization ReactJS SPA](#authorization-reactjs-spa)
  - [Authorization Python](#authorization-python)
  - [Authorization .NET Core](#authorization-.net-core)
  - [Authorization Java](#authorization-java)  

## Introduction

This folder contains examples on how to implement authorization in [KeyCloak](https://www.keycloak.org/) using the OpenID standart in .NET core, python and Java. The examples cover the implicit and authorization flows and also show how to deal with role based access.

An easy overview of the flows can be found [here](https://medium.com/google-cloud/understanding-oauth2-and-building-a-basic-authorization-server-of-your-own-a-beginners-guide-cf7451a16f66).

## Security concerns and concidirations

While the examples cover implicit flow it`s not recommanded for security concerns and should be avoided. You can read more [here](https://oauth.net/2/grant-types/implicit/).

To deploy the examples securely on a Kubernetes cluster have a look [here](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#create-a-pod-that-has-access-to-the-secret-data-through-environment-variables).

## Prerequisites

- **Keycloak**
  - Docker
- **React**
  - nodejs => 10.13.0
  - yarn => 1.12.3
  - create-react-app => 2.1.1
- **Python**
  - python 2.7.15
  - pipenv
- **Dotnet**
  - .Net SDK 2.1.6
- **Java**
  - JDK => 1.8

## Setup test instance of KeyCloak

This part describes the steps to setup a local KeyCloak instance for running the demos:

1. Start the local KeyCLoak container with:

    ```bash
    docker run -p 8080:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin jboss/keycloak
    ```

    This will start a new container running on port 8080. It will have the user `admin` with password `admin`.

2. Import the pre-prepared realm into the local KeyCloack container:

    - Goto <http://localhost:8080> and login to the administration console with the `admin` account.
    - Goto `Import` and select the `realm-export.json`. Set `If a resource exists` to `Skip`.

The master realm now has 2 clients (`demo-app-authorization`, `demo-app-implicit`) which both contain 2 roles (`Administrator`, `User`) which are used in the examples.

Note: Users should be added manually and assigned one of the 2 (`Administrator`, `User`) client roles for testing.

## Implicit flow examples

### Implicit ReactJS SPA

The .NET core, python and Java examples all relly on the same ReactJS SPA. This first needs to be build and deployed before any of the examples can be started:

- Open a terminal here `examples/keycloak/implicit/react`
- Run the following to provision the project:

    ```bash
    yarn install
    ```
- Run the following to build the project and copy the artifacts to the .NET core, python and Java examples:

    ```bash
    yarn build
    ```

### Implicit Python

The Python example is based on a [flask](http://flask.pocoo.org/) and uses [JoseJWT](https://github.com/mpdavis/python-jose) for validation.

To run the example:

- Open a terminal here `examples/keycloak/implicit/python`
- Run the following to provision and build the docker image:

    ```bash
    docker build -t python-implicit .
    ```
- Run the following to start a new container with the build image where `IP` in the url parameter needs to be replaced with the IP of the KeyCloak server:

    ```bash
    docker run -e realm="master" -e url="http://IP:8080/auth" -e clientid="demo-app-implicit" -p 8090:80 python-implicit
    ```

The example can then be opened here: <http://localhost:8090>

### Implicit .NET core

The .NET core example uses [IdentityServer4](http://docs.identityserver.io/en/latest/) todo the validation.

To run the example:

- Open a terminal here `examples/keycloak/implicit/dotnet/KeyCloak`
- Run the following to provision and build the docker image:

    ```bash
    docker build -t dotnet-implicit .
    ```
- Run the following to start a new container with the build image where `IP` in the url parameter needs to be replaced with the IP of the KeyCloak server:

    ```bash
    docker run -e realm="master" -e url="http://IP:8080/auth" -e clientid="demo-app-implicit" -p 8090:80 dotnet-implicit
    ```

The example can then be opened here: <http://localhost:8090>

### Implicit Java

The Java example uses [Spring Boot](http://spring.io/projects/spring-boot) with [WebFlux](https://docs.spring.io/spring/docs/current/spring-framework-reference/web-reactive.html).

To run the example:

- Open a terminal here `examples/keycloak/implicit/java`
- Run the following to provision and build the docker image:

    ```bash
    docker build -t java-implicit .
    ```
- Run the following to start a new container with the build image where `IP` in the url parameter needs to be replaced with the IP of the KeyCloak server:

    ```bash
    docker run -e realm="master" -e url="http://IP:8080/auth" -e clientid="demo-app-implicit" -p 8090:8090 java-implicit
    ```

The example can then be opened here: <http://localhost:8090>

## Authorization flow examples

 It might be the case that after the import of the `realm-export.json` the secret clientkey of `demo-app-authorization` needs to be reset. This can be done here in the KeyCloak administrator console:

`Clients` > `demo-app-authorization` > `Credentials` > `Regenerate Secret`

### Authorization ReactJS SPA

The .NET core, python and Java examples all relly on the same ReactJS SPA. This first needs to be build and deployed before any of the examples can be started:

- Open a terminal here `examples/keycloak/authorization/react`
- Run the following to provision the project:

    ```bash
    yarn install
    ```
- Run the following to build the project and copy the artifacts to the .NET core, python and Java examples:

    ```bash
    yarn build
    ```

### Authorization Python

The Python example is based on a [flask](http://flask.pocoo.org/) and uses [flas-oidc](https://flask-oidc.readthedocs.io/en/latest/) for validation.

To run the example:

- Open a terminal here `examples/keycloak/authorization/python`
- Run the following to provision and build the docker image:

    ```bash
    docker build -t python-authorization .
    ```
- Run the following to start a new container with the build image where `IP` in the url parameter needs to be replaced with the IP of the KeyCloak server and `SECRET` in the clientsecret parameter needs to be replaced with the clients secret:

    ```bash
    docker run -e realm="master" -e url="http://IP:8080/auth" -e clientid="demo-app-authorization" -e clientsecret="SECRET" -p 8090:80 python-authorization
    ```

The example can then be opened here: <http://localhost:8090>

### Authorization .NET core

The .NET core example uses [IdentityServer4](http://docs.identityserver.io/en/latest/) todo the validation.

To run the example:

- Open a terminal here `examples/keycloak/authorization/dotnet/KeyCloak`
- Run the following to provision and build the docker image:

    ```bash
    docker build -t dotnet-authorization .
    ```
- Run the following to start a new container with the build image where `IP` in the url parameter needs to be replaced with the IP of the KeyCloak server and `SECRET` in the clientsecret parameter needs to be replaced with the clients secret:

    ```bash
    docker run -e realm="master" -e url="http://IP:8080/auth" -e clientid="demo-app-authorization" -e clientsecret="SECRET" -p 8090:80 dotnet-authorization
    ```

The example can then be opened here: <http://localhost:8090>

### Authorization Java

The Java example uses [Spring Boot](http://spring.io/projects/spring-boot) with [WebFlux](https://docs.spring.io/spring/docs/current/spring-framework-reference/web-reactive.html).

To run the example:

- Open a terminal here `examples/keycloak/authorization/java`
- Run the following to provision and build the docker image:

    ```bash
    docker build -t java-authorization .
    ```
- Run the following to start a new container with the build image where `IP` in the url parameter needs to be replaced with the IP of the KeyCloak server and `SECRET` in the clientsecret parameter needs to be replaced with the clients secret:

    ```bash
    docker run -e realm="master" -e url="http://IP:8080/auth" -e clientid="demo-app-authorization" -e clientsecret="SECRET" -p 8090:80 java-authorization
    ```

The example can then be opened here: <http://localhost:8090>