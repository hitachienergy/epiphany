from tests.mocks.command_run_mock import CommandRunMock

from src.command.yum_config_manager import YumConfigManager


def test_interface_enable_repo(mocker):
    ''' Check argument construction for `yum-config-manager --enable` '''
    with CommandRunMock(mocker, YumConfigManager(1).enable_repo, {'repo': 'some_repo'}) as call_args:
        assert call_args == ['yum-config-manager', '--enable', 'some_repo']


def test_interface_add_repo(mocker):
    ''' Check argument construction for `yum-config-manager --add-repo` '''
    with CommandRunMock(mocker, YumConfigManager(1).add_repo, {'repo': 'some_repo'}) as call_args:
        assert call_args == ['yum-config-manager', '--add-repo', 'some_repo']


def test_interface_disable_repo(mocker):
    ''' Check argument construction for `yum-config-manager --disable` '''
    with CommandRunMock(mocker, YumConfigManager(1).disable_repo, {'repo': 'some_repo'}) as call_args:
        assert call_args == ['yum-config-manager', '--disable', 'some_repo']
