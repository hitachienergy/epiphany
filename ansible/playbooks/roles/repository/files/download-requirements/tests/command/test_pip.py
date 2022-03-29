from tests.mocks.command_run_mock import CommandRunMock

from src.command.pip import Pip


def test_interface_install(mocker):
    ''' Check argument construction for `pip install` '''
    with CommandRunMock(mocker, Pip(1).install, {'package': 'PyYAML',
                                                 'version': '==6.0',
                                                 'user': True}) as call_args:
        assert call_args == ['pip3', 'install', 'PyYAML==6.0', '--user']
