#!/bin/bash -eu

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
echo "deb https://artifacts.elastic.co/packages/oss-6.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-6.x.list

wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | apt-key add -
echo "deb [arch=amd64] https://packages.elastic.co/curator/5/debian stable main" | tee /etc/apt/sources.list.d/elastic-curator-6.x.list

wget -qO - https://packages.grafana.com/gpg.key | apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | tee /etc/apt/sources.list.d/grafana.list

wget -qO - https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list

wget -qO - https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc | apt-key add -
echo "deb https://packages.erlang-solutions.com/ubuntu bionic contrib" | tee /etc/apt/sources.list.d/erlang-23.x.list

wget -qO - https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey | apt-key add -
echo "deb https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu bionic main" | tee /etc/apt/sources.list.d/rabbitmq.list

wget -qO -  https://download.docker.com/linux/ubuntu/gpg | apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable" | tee /etc/apt/sources.list.d/docker-ce.list

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
echo "deb https://artifacts.elastic.co/packages/oss-7.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-7.x.list

wget -qO - https://d3g5vo6xdbdb9a.cloudfront.net/GPG-KEY-opendistroforelasticsearch | sudo apt-key add -
echo "deb https://d3g5vo6xdbdb9a.cloudfront.net/apt stable main" | tee -a   /etc/apt/sources.list.d/opendistroforelasticsearch.list

wget -qO - https://dl.2ndquadrant.com/gpg-key.asc | apt-key add -
echo "deb https://dl.2ndquadrant.com/default/release/apt bionic-2ndquadrant main" | tee -a /etc/apt/sources.list.d/2ndquadrant-dl-default-release.list

apt update
