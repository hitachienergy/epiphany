from pathlib import Path

from tests.mocks.command_run_mock import CommandRunMock

from src.command.debian.apt_key import AptKey


def test_interface_add(mocker):
    ''' Check argument construction for `apt-key add` '''
    with CommandRunMock(mocker, AptKey(1).add, {'key': Path('/path/to/some/key')}) as call_args:
        assert call_args == ['apt-key', 'add', '/path/to/some/key']
