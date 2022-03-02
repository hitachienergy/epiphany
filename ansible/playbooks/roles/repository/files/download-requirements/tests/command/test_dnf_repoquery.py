from tests.mocks.command_run_mock import CommandRunMock

from src.command.dnf_repoquery import DnfRepoquery


def test_interface_query(mocker):
    ''' Check argument construction for `dnf repoquery` - generic query '''
    with CommandRunMock(mocker, DnfRepoquery(1).query, {'package': 'vim',
                                                        'queryformat': 'some_format',
                                                        'archlist': ['some_arch', 'noarch']}) as call_args:
        assert call_args == ['dnf',
                             'repoquery',
                             '--archlist=some_arch,noarch',
                             '--assumeyes',
                             '--latest-limit=1',
                             '--queryformat=some_format',
                             '--quiet',
                             'vim'
                            ]

def test_interface_get_dependencies(mocker):
    ''' Check argument construction for `repoquery` - dependencies query '''
    with CommandRunMock(mocker, DnfRepoquery(1).get_dependencies, {'package': 'vim',
                                                                   'queryformat': 'some_format',
                                                                   'archlist': ['some_arch', 'noarch']}) as call_args:
        assert call_args == ['dnf',
                             'repoquery',
                             '--archlist=some_arch,noarch',
                             '--assumeyes',
                             '--latest-limit=1',
                             '--queryformat=some_format',
                             '--quiet',
                             '--requires',
                             '--resolve',
                             'vim'
                            ]
