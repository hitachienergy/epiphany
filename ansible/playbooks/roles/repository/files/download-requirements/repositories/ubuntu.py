from pathlib import Path
from typing import Dict


class Repo:
    def __init__(self, key: str, content: str, path: Path):
        self.key: str = key
        self.content: str = content
        self.path: Path = path


REPOSITORIES_X86_64: Dict[str, Repo] = {
    'elastic_6': Repo('https://artifacts.elastic.co/GPG-KEY-elasticsearch',
                      'deb https://artifacts.elastic.co/packages/oss-6.x/apt stable main',
                      Path('/etc/apt/sources.list.d/elastic-6.x.list')),

    'kubernetes': Repo('https://packages.cloud.google.com/apt/doc/apt-key.gpg',
                       'deb http://apt.kubernetes.io/ kubernetes-xenial main',
                       Path('/etc/apt/sources.list.d/kubernetes.list')),

    'erlang_solutions': Repo('https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc',
                             'deb https://packages.erlang-solutions.com/ubuntu bionic contrib',
                             Path('/etc/apt/sources.list.d/erlang-23.x.list')),

    'rabbitmq_server': Repo('https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey',
                            'deb https://packagecloud.io/rabbitmq/rabbitmq-server/ubuntu bionic main',
                            Path('/etc/apt/sources.list.d/rabbitmq.list')),

    'docker_ce': Repo('https://download.docker.com/linux/ubuntu/gpg',
                      'deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable',
                      Path('/etc/apt/sources.list.d/docker-ce.list')),

    'elastic_7': Repo('https://artifacts.elastic.co/GPG-KEY-elasticsearch',
                      'deb https://artifacts.elastic.co/packages/oss-7.x/apt stable main',
                      Path('/etc/apt/sources.list.d/elastic-7.x.list')),

    'opendistroforelasticsearch': Repo('https://d3g5vo6xdbdb9a.cloudfront.net/GPG-KEY-opendistroforelasticsearch',
                                       'deb https://d3g5vo6xdbdb9a.cloudfront.net/apt stable main',
                                       Path('/etc/apt/sources.list.d/opendistroforelasticsearch.list')),

    'postgresql': Repo('https://www.postgresql.org/media/keys/ACCC4CF8.asc',
                       'deb http://apt.postgresql.org/pub/repos/apt bionic-pgdg main',
                       Path('/etc/apt/sources.list.d/pgdg.list')),

    # Historical packages from apt.postgresql.org
    'postgresql-archive': Repo('https://www.postgresql.org/media/keys/ACCC4CF8.asc',
                               'deb http://apt-archive.postgresql.org/pub/repos/apt bionic-pgdg-archive main',
                               Path('/etc/apt/sources.list.d/pgdg-archive.list')),

    # Provides repmgr
    '2ndquadrant': Repo('https://dl.2ndquadrant.com/gpg-key.asc',
                        'deb https://dl.2ndquadrant.com/default/release/apt bionic-2ndquadrant main',
                        Path('/etc/apt/sources.list.d/2ndquadrant-dl-default-release.list'))
}
