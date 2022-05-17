from tests.mocks.command_run_mock import CommandRunMock

from src.command.redhat.dnf_config_manager import DnfConfigManager


def test_interface_add_repo(mocker):
    ''' Check argument construction for `dnf config-manager --add-repo` '''
    with CommandRunMock(mocker, DnfConfigManager(1).add_repo, {'repo': 'some_repo'}) as call_args:
        assert call_args == ['dnf', 'config-manager', '--add-repo', 'some_repo']


def test_interface_disable_repo(mocker):
    ''' Check argument construction for `dnf config-manager --set-disabled` '''
    with CommandRunMock(mocker, DnfConfigManager(1).disable_repo, {'repo': 'some_repo'}) as call_args:
        assert call_args == ['dnf', 'config-manager', '--set-disabled', 'some_repo']


def test_interface_enable_repo(mocker):
    ''' Check argument construction for `dnf config-manager --set-enabled` '''
    with CommandRunMock(mocker, DnfConfigManager(1).enable_repo, {'repo': 'some_repo'}) as call_args:
        assert call_args == ['dnf', 'config-manager', '--set-enabled', 'some_repo']
