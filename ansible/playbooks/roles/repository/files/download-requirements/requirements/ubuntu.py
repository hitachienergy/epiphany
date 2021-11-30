from typing import Dict, List
from requirements.crane import CRANE
from requirements.files import FILES
from requirements.images import IMAGES


REQUIREMENTS_X86_64: Dict[str, List] = {
    'crane': CRANE,
    'packages': [
        'adduser',
        'apt-transport-https',
        'auditd',
        'bash-completion',
        'build-essential',
        'ca-certificates',
        'cifs-utils',
        'containerd.io',
        'cri-tools=1.13.0*',
        'curl',
        'docker-ce=5:20.10.8*',
        'docker-ce-cli=5:20.10.8*',
        'docker-ce-rootless-extras=5:20.10.8*',
        'ebtables',
        # for opendistroforelasticsearch & logging roles
        'elasticsearch-oss=7.10.2*',

        # Erlang packages must be compatible with RabbitMQ version.
        # Metapackages such as erlang and erlang-nox must only be used
        # with apt version pinning. They do not pin their dependency versions.
        # List based on: https://www.rabbitmq.com/install-debian.html#installing-erlang-package
        'erlang-asn1=1:23.1.5*',
        'erlang-base=1:23.1.5*',
        'erlang-crypto=1:23.1.5*',
        'erlang-eldap=1:23.1.5*',
        'erlang-ftp=1:23.1.5*',
        'erlang-inets=1:23.1.5*',
        'erlang-mnesia=1:23.1.5*',
        'erlang-os-mon=1:23.1.5*',
        'erlang-parsetools=1:23.1.5*',
        'erlang-public-key=1:23.1.5*',
        'erlang-runtime-tools=1:23.1.5*',
        'erlang-snmp=1:23.1.5*',
        'erlang-ssl=1:23.1.5*',
        'erlang-syntax-tools=1:23.1.5*',
        'erlang-tftp=1:23.1.5*',
        'erlang-tools=1:23.1.5*',
        'erlang-xmerl=1:23.1.5*',

        'ethtool',
        'filebeat=7.9.2*',
        'firewalld',
        'fping',
        'gnupg2',
        'haproxy',
        'htop',
        'iftop',
        'jq',
        'libfontconfig1',
        'logrotate',
        'logstash-oss=1:7.12.0*',
        'netcat',
        'net-tools',
        'nfs-common',
        'opendistro-alerting=1.13.1*',
        'opendistro-index-management=1.13.1*',
        'opendistro-job-scheduler=1.13.0*',
        'opendistro-performance-analyzer=1.13.0*',
        'opendistro-security=1.13.1*',
        'opendistro-sql=1.13.0*',
        'opendistroforelasticsearch-kibana=1.13.1*',
        'openjdk-8-jre-headless',
        'openssl',
        'postgresql-13',
        'python-pip',
        'python-psycopg2',
        'python-selinux',
        'python-setuptools',
        'rabbitmq-server=3.8.9*',
        'smbclient',
        'samba-common',
        'smbclient',
        'software-properties-common',
        'sshpass',
        'sysstat',
        'tar',
        'telnet',
        'tmux',
        'unzip',
        'vim',

        # to make remote-to-remote "synchronize" work in ansible
        'rsync',

        # for curl, issue #869
        'libcurl4',

        # for openjdk-8-jre-headless
        'libnss3',
        'libcups2',
        'libavahi-client3',
        'libavahi-common3',
        'libjpeg8',
        'libfontconfig1',
        'libxtst6',
        'fontconfig-config',

        'python-apt',

        # for python-selinux
        'python',
        'python2.7',
        'python-minimal',
        'python2.7-minimal',

        # for build-essential
        'gcc',
        'gcc-7',
        'g++',
        'g++-7',
        'dpkg-dev',
        'libc6-dev',
        'cpp',
        'cpp-7',
        'libgcc-7-dev',
        'binutils',
        'gcc-8-base',

        # for rabbit/erlang
        'libodbc1',

        # for air-gap repo installation
        'apache2',
        'apache2-bin',
        'apache2-utils',

        # for jq
        'libjq1',

        # for gnupg2
        'gnupg',
        'gpg',
        'gpg-agent',

        # for azure
        'smbclient',
        'samba-libs',
        'libsmbclient',

        # postgres related packages
        # if version is not specified, it's not related to postgres version and the latest is used
        'pgbouncer=1.16.0*',
        'pgdg-keyring',
        'postgresql-13-pgaudit=1.5.0*',
        'postgresql-10-repmgr=5.2.1*',
        'postgresql-13-repmgr=5.2.1*',
        'postgresql-client-13',
        'postgresql-client-common',
        'postgresql-common',
        'repmgr-common=5.2.1*',

        # for firewalld
        'ipset',
        'libipset3',
        'python3-decorator',
        'python3-selinux',
        'python3-slip',
        'python3-slip-dbus',
        # for ansible module postgresql_query in role postgres-exporter
        'libpq5',
        'python3-psycopg2',
        'python3-jmespath',

        # for vim, issue #869
        'libpython3.6',

        # for Ansible (certificate modules)
        'python-cryptography',

        # for python-cryptography
        'python-asn1crypto',
        'python-cffi-backend',
        'python-enum34',
        'python-idna',
        'python-ipaddress',
        'python-six',

        # K8s v1.18.6 (Epiphany >= v0.7.1)
        'kubeadm=1.18.6*',
        'kubectl=1.18.6*',
        'kubelet=1.18.6*',

        # K8s v1.19.15 (Epiphany >= v1.3, transitional version)
        'kubeadm=1.19.15*',
        'kubectl=1.19.15*',
        'kubelet=1.19.15*',

        # K8s v1.20.12
        'kubeadm=1.20.12*',
        'kubectl=1.20.12*',
        'kubelet=1.20.12*',

        # Kubernetes Generic
        # kubernetes-cni-0.8.6 since K8s v1.18.6
        'kubernetes-cni=0.8.6-00*',
        # kubernetes-cni-0.8.7 since K8s v1.19.15
        'kubernetes-cni=0.8.7-00*',
    ],
    'files': FILES + [
        # --- Packages ---
        # Switched from APT repo because there was only one (the latest) version available (issue #2262)
        'https://packages.elastic.co/curator/5/debian9/pool/main/e/elasticsearch-curator/elasticsearch-curator_5.8.3_amd64.deb',
        # Grafana package is not downloaded from repository since it was not reliable (issue #2449)
        'https://dl.grafana.com/oss/release/grafana_7.3.5_amd64.deb',

    ],
    'images': IMAGES
}
