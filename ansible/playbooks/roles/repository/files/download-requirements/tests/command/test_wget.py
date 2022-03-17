from pathlib import Path

from src.command.wget import IPFamily, Wget
from tests.mocks.command_run_mock import CommandRunMock


def test_builder_download(mocker):
    ''' Check argument construction for `wget` '''
    with CommandRunMock(mocker, Wget(1).download, {'url': 'http://some.url.com',
                                                   'output_document': Path('/var/log/output_name'),
                                                   'directory_prefix': Path('/custom/prefix'),
                                                   'ip_family': IPFamily.IPV4}) as call_args:
        assert call_args == ['wget', '--no-use-server-timestamps', '--show-progress',
                             '--output-document=/var/log/output_name', '--directory-prefix=/custom/prefix',
                             '--prefer-family=IPv4', 'http://some.url.com']
