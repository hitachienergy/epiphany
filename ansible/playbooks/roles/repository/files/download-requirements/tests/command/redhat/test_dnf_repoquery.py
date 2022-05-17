from tests.mocks.command_run_mock import CommandRunMock

from src.command.redhat.dnf_repoquery import DnfRepoquery


def test_interface_query(mocker):
    ''' Check argument construction for `dnf repoquery` - generic query '''
    with CommandRunMock(mocker, DnfRepoquery(1).query, {'packages': ['tar', 'vim'],
                                                        'queryformat': 'some_format',
                                                        'archlist': ['some_arch', 'noarch']}) as call_args:
        assert call_args == ['dnf',
                             'repoquery',
                             '--archlist=some_arch,noarch',
                             '--disableplugin=subscription-manager',
                             '--latest-limit=1',
                             '--queryformat=some_format',
                             'tar',
                             'vim'
                            ]

def test_interface_get_dependencies(mocker):
    ''' Check argument construction for `repoquery` - dependencies query '''
    with CommandRunMock(mocker, DnfRepoquery(1).get_dependencies, {'packages': ['tar', 'vim'],
                                                                   'queryformat': 'some_format',
                                                                   'archlist': ['some_arch', 'noarch']}) as call_args:
        assert call_args == ['dnf',
                             'repoquery',
                             '--archlist=some_arch,noarch',
                             '--disableplugin=subscription-manager',
                             '--latest-limit=1',
                             '--queryformat=some_format',
                             '--requires',
                             '--resolve',
                             'tar',
                             'vim'
                            ]
