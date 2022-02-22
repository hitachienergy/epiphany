from tests.mocks.command_run_mock import CommandRunMock

from src.command.repoquery import Repoquery


def test_interface_query(mocker):
    ''' Check argument construction for `repoquery` '''
    with CommandRunMock(mocker, Repoquery(1).query, {'package': 'vim',
                                                     'queryformat': 'some_format',
                                                     'arch': 'some_arch',
                                                     'requires': True,
                                                     'resolve': True}) as call_args:
        assert call_args == ['repoquery',
                             '--requires',
                             '--resolve',
                             '--queryformat',
                             'some_format',
                             '--archlist=some_arch,noarch',
                             'vim'
                            ]
