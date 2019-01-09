# Epiphany Web App

Dotnet core web application for Epiphany demo purposes. Solution is built from 3 important parts:
<!-- TOC -->

- [Epiphany Web App](#epiphany-web-app)
    - [Docker compose](#docker-compose)
    - [Kubernetes configurations](#kubernetes-configurations)
    - [ASP.NET Core application](#aspnet-core-application)

<!-- /TOC -->

## Docker compose

In epiphany-web-app solution there is docker-compose project which responsibility is to manage multi image solutions. Image is build using Dockerfile located inside epiphany-web-app project. You can use Visual Studio to build and run web project or using following command to let Docker do that.

`docker build -f ./epiphany-web-app/Dockerfile -t epiphany-web .`

Important thing is to set working directory to `.sln` file directory, it will be used as building context.

When build and image you can inspect it exists using:
`docker images`  

Having image built successfully you need to tag and push image to your Docker repository.
`docker tag YOUR_IMAGE_ID your-docker-repository.io/epiphany-web`  

And then:
`docker push your-docker-repository.io/epiphany-web`

## Kubernetes configurations

Definition for Kubernetes deployment is located in `.yml` file. It contains information about docker image repository from which Kubernetes will pull image. Before creating a deployment, you need to update this file with Docker repository address and secret name (fields `image: your-docker-repository.azurecr.io/epiphany-web` and `- name: regcred`)

When ready, you can apply/create deployment on kubernetes using kubectl command:

`kubectl create -f ./epiphany-web-app/kubernetes-configs/deploy.yml`

Successful deployment will result in availability of Epiphany Web App. Default address of app will look like following:
`http://your-master-node-address:30001`

Port 30001 is default value, you can change it in yml file.

## ASP.NET Core application

Demo application build using ASP.NET and Linux image (yes, it can run both: Linux and Windows). Web application is a simple MVC app that contains useful links and graphics about Epiphany.
