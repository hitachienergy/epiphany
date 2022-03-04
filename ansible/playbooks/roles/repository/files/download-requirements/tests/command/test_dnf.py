from tests.mocks.command_run_mock import CommandRunMock

from src.command.dnf import Dnf


def test_interface_update(mocker):
    ''' Check argument construction for `dnf update` '''
    with CommandRunMock(mocker, Dnf(1).update, {'enablerepo': 'some_repo',
                                                'package': 'some_package',
                                                'disablerepo': 'other_repo',
                                                'assume_yes': True}) as call_args:
        assert call_args == ['dnf' , 'update', '-y', 'some_package', '--disablerepo=other_repo', '--enablerepo=some_repo']


def test_interface_install(mocker):
    ''' Check argument construction for `dnf install` '''
    with CommandRunMock(mocker, Dnf(1).install, {'package': 'vim'}) as call_args:
        assert call_args == ['dnf' , 'install', '-y', 'vim']


def test_interface_remove(mocker):
    ''' Check argument construction for `dnf remove` '''
    with CommandRunMock(mocker, Dnf(1).remove, {'package': 'vim'}) as call_args:
        assert call_args == ['dnf' , 'remove', '-y', 'vim']


def test_interface_is_repo_enabled(mocker):
    ''' Check argument construction for `dnf repolist enabled` '''
    with CommandRunMock(mocker, Dnf(1).is_repo_enabled, {'repo': 'some_repo'}) as call_args:
        assert call_args == ['dnf' , 'repolist', '--enabled']


def test_interface_find_rhel_repo_id(mocker):
    ''' Check argument construction for `dnf repolist all` '''
    with CommandRunMock(mocker, Dnf(1).find_rhel_repo_id, {'patterns': ['pat1', 'pat2']}) as call_args:
        assert call_args == ['dnf' , 'repolist', '--all', '--quiet']
