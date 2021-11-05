from tests.mocks.command_run_mock import CommandRunMock

from src.command.yum import Yum


def test_builder_install(mocker):
    ''' Check argument construction for `yum install -y` '''
    with CommandRunMock(mocker, Yum(1).install, {'package': 'vim', 'assume_yes': True}) as call_args:
        assert call_args == ['yum', 'install', '-y', 'vim']

