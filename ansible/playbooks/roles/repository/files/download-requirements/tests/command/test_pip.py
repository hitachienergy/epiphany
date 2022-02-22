from tests.mocks.command_run_mock import CommandRunMock

from src.command.pip import Pip


def test_interface_install(mocker):
    ''' Check argument construction for `pip install` '''
    with CommandRunMock(mocker, Pip(1).install, {'package': 'poyo',
                                                 'version': '=0.5.0',
                                                 'user': True}) as call_args:
        assert call_args == ['pip3', 'install', 'poyo=0.5.0', '--user']
