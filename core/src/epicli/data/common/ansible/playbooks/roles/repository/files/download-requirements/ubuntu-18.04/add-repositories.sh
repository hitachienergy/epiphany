#!/bin/bash

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
echo "deb https://artifacts.elastic.co/packages/oss-6.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-6.x.list

wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | apt-key add -
echo "deb [arch=amd64] https://packages.elastic.co/curator/5/debian stable main" | tee /etc/apt/sources.list.d/elastic-curator-6.x.list

wget -qO - https://packages.grafana.com/gpg.key | apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | tee /etc/apt/sources.list.d/grafana.list

wget -qO - https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list

wget -qO - https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | apt-key add -
echo "deb http://dl.bintray.com/rabbitmq-erlang/debian bionic erlang-21.x" | tee /etc/apt/sources.list.d/erlang-21.x.list
echo "deb https://dl.bintray.com/rabbitmq/debian bionic main" | tee /etc/apt/sources.list.d/rabbitmq.list

wget -qO -  https://download.docker.com/linux/ubuntu/gpg | apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable" | tee /etc/apt/sources.list.d/docker-ce.list

apt update
