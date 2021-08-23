#!/usr/bin/env bash -eu

DOCKER_CE_PATCHED_REPO_CONF=$(cat <<'EOF'
[docker-ce-stable-patched]
name=Docker CE Stable - patched centos/7/$basearch/stable
baseurl=https://download.docker.com/linux/centos/7/$basearch/stable
enabled=1
gpgcheck=1
gpgkey=https://download.docker.com/linux/centos/gpg
EOF
)

ELASTIC_6_REPO_CONF=$(cat <<'EOF'
[elastic-6]
name=Elastic repository for 6.x packages
baseurl=https://artifacts.elastic.co/packages/oss-6.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF
)

ELASTICSEARCH_7_REPO_CONF=$(cat <<'EOF'
[elasticsearch-7.x]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/oss-7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF
)

ELASTICSEARCH_CURATOR_REPO_CONF=$(cat <<'EOF'
[curator-5]
name=CentOS/RHEL 7 repository for Elasticsearch Curator 5.x packages
baseurl=https://packages.elastic.co/curator/5/centos/7
gpgcheck=1
gpgkey=https://packages.elastic.co/GPG-KEY-elasticsearch
enabled=1
EOF
)

KUBERNETES_REPO_CONF=$(cat <<'EOF'
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
)

OPENDISTRO_REPO_CONF=$(cat <<'EOF'
[opendistroforelasticsearch-artifacts-repo]
name=Release RPM artifacts of OpenDistroForElasticsearch
baseurl=https://d3g5vo6xdbdb9a.cloudfront.net/yum/noarch/
enabled=1
gpgkey=https://d3g5vo6xdbdb9a.cloudfront.net/GPG-KEY-opendistroforelasticsearch
gpgcheck=1
repo_gpgcheck=1
autorefresh=1
type=rpm-md
EOF
)

POSTGRESQL_REPO_CONF=$(cat <<'EOF'
[pgdg13]
name=PostgreSQL 13 for RHEL/CentOS $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/13/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG
EOF
)

POSTGRESQL_COMMON_REPO_CONF=$(cat <<'EOF'
[pgdg-common]
name=PostgreSQL common for RHEL/CentOS $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/common/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://download.postgresql.org/pub/repos/yum/RPM-GPG-KEY-PGDG
EOF
)

RABBITMQ_SERVER_REPO_CONF=$(cat <<'EOF'
[rabbitmq-server]
name=rabbitmq-rpm
baseurl=https://packagecloud.io/rabbitmq/rabbitmq-server/el/7/$basearch
gpgcheck=1
gpgkey=https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey
repo_gpgcheck=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
enabled=1
EOF
)

# Official Docker CE repository, added with https://download.docker.com/linux/centos/docker-ce.repo,
# has broken URL (https://download.docker.com/linux/centos/7Server/x86_64/stable) for longer time.
# So direct (patched) link is used first if available.
add_repo_as_file 'docker-ce-stable-patched' "$DOCKER_CE_PATCHED_REPO_CONF"
if ! is_repo_available "docker-ce-stable-patched"; then
	disable_repo "docker-ce-stable-patched"
	add_repo 'docker-ce' 'https://download.docker.com/linux/centos/docker-ce.repo'
fi
add_repo_as_file 'elastic-6' "$ELASTIC_6_REPO_CONF"
add_repo_as_file 'elasticsearch-7' "$ELASTICSEARCH_7_REPO_CONF"
add_repo_as_file 'elasticsearch-curator-5' "$ELASTICSEARCH_CURATOR_REPO_CONF"
add_repo_as_file 'kubernetes' "$KUBERNETES_REPO_CONF"
add_repo_as_file 'opendistroforelasticsearch' "$OPENDISTRO_REPO_CONF"
add_repo_as_file 'postgresql-13' "$POSTGRESQL_REPO_CONF"
add_repo_as_file 'postgresql-common' "$POSTGRESQL_COMMON_REPO_CONF" # for pgbouncer
add_repo_as_file 'rabbitmq' "$RABBITMQ_SERVER_REPO_CONF"
