#!/usr/bin/env bash -eu

RABBITMQ_ERLANG_REPO_CONF=$(cat <<'EOF'
[rabbitmq-erlang]
name=rabbitmq-erlang
baseurl=https://dl.bintray.com/rabbitmq-erlang/rpm/erlang/23/el/7
gpgcheck=1
gpgkey=https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc
repo_gpgcheck=1
enabled=1
deltarpm_percentage=0
EOF
)

add_repo_as_file 'rabbitmq-erlang' "$RABBITMQ_ERLANG_REPO_CONF"
add_repo_from_script 'https://dl.2ndquadrant.com/default/release/get/10/rpm'
disable_repo '2ndquadrant-dl-default-release-pg10-debug'
