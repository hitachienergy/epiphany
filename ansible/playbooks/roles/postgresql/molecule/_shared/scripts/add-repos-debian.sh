#!/bin/bash -eu

apt update && apt -y install wget gpg-agent

wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt focal-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
echo "deb http://apt-archive.postgresql.org/pub/repos/apt focal-pgdg-archive main" | tee -a /etc/apt/sources.list.d/pgdg.list

apt update
