from tests.mocks.command_run_mock import CommandRunMock

from src.command.repoquery import Repoquery


def test_interface_query(mocker):
    ''' Check argument construction for `repoquery` - generic query '''
    with CommandRunMock(mocker, Repoquery(1).query, {'package': 'vim',
                                                     'queryformat': 'some_format',
                                                     'arch': 'some_arch'}) as call_args:
        assert call_args == ['repoquery',
                             '--queryformat',
                             'some_format',
                             '--archlist=some_arch,noarch',
                             'vim']

def test_interface_get_dependencies(mocker):
    ''' Check argument construction for `repoquery` - dependencies query '''
    with CommandRunMock(mocker, Repoquery(1).get_dependencies, {'package': 'vim',
                                                                'queryformat': 'some_format',
                                                                'arch': 'some_arch'}) as call_args:
        assert call_args == ['repoquery',
                             '--requires',
                             '--resolve',
                             '--queryformat',
                             'some_format',
                             '--archlist=some_arch,noarch',
                             'vim']
