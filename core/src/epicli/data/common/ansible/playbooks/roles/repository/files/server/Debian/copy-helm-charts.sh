#!/bin/bash -eu

EPI_REPO_SERVER_PATH=$1 # /var/www/html/epirepo is the default

echo "copying helm charts to web server..."
mkdir -p ${EPI_REPO_SERVER_PATH}/charts
cp -r /tmp/epi-repository-charts/* ${EPI_REPO_SERVER_PATH}/charts/