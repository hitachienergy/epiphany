APT_CACHE_DEPENDS_SOLR_STDOUT = '''
solr-common
  Depends: curl
  Depends: debconf
 |Depends: default-jre-headless
 |Depends: <java5-runtime-headless>
    default-jre-headless
    openjdk-11-jre-headless
    openjdk-13-jre-headless
    openjdk-16-jre-headless
    openjdk-17-jre-headless
    openjdk-8-jre-headless
  Depends: <java6-runtime-headless>
    default-jre-headless
    openjdk-11-jre-headless
    openjdk-13-jre-headless
    openjdk-16-jre-headless
    openjdk-17-jre-headless
    openjdk-8-jre-headless
  Depends: libjs-jquery
'''

APT_CACHE_DEPENDS_RABBITMQ_STDOUT = '''
rabbitmq-server
  Depends: adduser
 |Depends: erlang-base
  Depends: erlang-base-hipe
  Depends: erlang-crypto
  Depends: erlang-eldap
  Depends: <python3:any>
    python3
    dummy
'''

APT_CACHE_DEPENDS_DATA = [
    ('tar', 'tar\n', []),
    ('solr-common', APT_CACHE_DEPENDS_SOLR_STDOUT, ['curl',
                                                    'debconf',
                                                    'default-jre-headless',
                                                    'libjs-jquery']),
    ('rabbitmq-server', APT_CACHE_DEPENDS_RABBITMQ_STDOUT, ['adduser',
                                                            'erlang-base',
                                                            'erlang-crypto',
                                                            'erlang-eldap',
                                                            'python3'])
]
