from tests.mocks.command_run_mock import CommandRunMock

from src.command.yum import Yum


# def test_builder_update(mocker):
    # ''' Check argument construction for `yum update -y` '''
    # with CommandRunMock(mocker, Yum(1).update, {'package': 'vim'}) as call_args:
        # assert call_args == ['yum', 'download', 'vim']


def test_builder_install(mocker):
    ''' Check argument construction for `yum install -y` '''
    with CommandRunMock(mocker, Yum(1).install, {'package': 'vim', 'assume_yes': True}) as call_args:
        assert call_args == ['yum', 'install', '-y', 'vim']

