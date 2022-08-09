from tests.mocks.command_run_mock import CommandRunMock

from src.command.redhat.rpm import Rpm


def test_interface_is_package_installed(mocker):
    ''' Check argument construction for `rpm --query` '''
    with CommandRunMock(mocker, Rpm(1).is_package_installed, {'package': 'vim'}) as call_args:
        assert call_args == ['rpm', '--query', '--quiet', 'vim']


def test_interface_import_key(mocker):
    ''' Check argument construction for `rpm --import` '''
    with CommandRunMock(mocker, Rpm(1).import_key, {'key': 'some_key'}) as call_args:
        assert call_args == ['rpm', '--import', 'some_key']


def test_interface_get_package_capabilities(mocker):
    ''' Check argument construction for `rpm -q --provides` '''
    with CommandRunMock(mocker, Rpm(1).get_package_capabilities, {'filename': 'some_file'}) as call_args:
        assert call_args == ['rpm', '-q', '--provides', 'some_file']


def test_interface_which_packages_provides_file(mocker):
    ''' Check argument construction for `rpm -q --whatprovides` '''
    with CommandRunMock(mocker, Rpm(1).which_packages_provides_file, {'filename': 'some_file'}) as call_args:
        assert call_args == ['rpm', '-q', '--whatprovides', 'some_file']
