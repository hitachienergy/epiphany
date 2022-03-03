from pathlib import Path

from tests.mocks.command_run_mock import CommandRunMock
from src.command.tar import Tar


def test_interface_pack(mocker):
    ''' Check argument construction for `tar -cf` '''
    with CommandRunMock(mocker, Tar().pack, {'filename': '/tmp/package.tar.gz',
                                             'targets': [Path('*')],
                                             'compress': True,
                                             'verbose': True,
                                             'preserve': True,
                                             'absolute_names': True,
                                             'directory': Path('/some/directory'),
                                             'verify': True}) as call_args:
        assert call_args == ['tar', '-czvpf', '/tmp/package.tar.gz',
                             '--absolute-names', '--directory', '/some/directory', '--verify', '*']


def test_interface_unpack(mocker):
    ''' Check argument construction for `tar -xf` '''
    with CommandRunMock(mocker, Tar().unpack, {'filename': Path('/tmp/package.tar.gz'),
                                               'target': Path('some_target'),
                                               'absolute_names': True,
                                               'directory': Path('/some/directory'),
                                               'overwrite': True,
                                               'verbose': True,
                                               'uncompress': True,
                                               'strip_components': 2}) as call_args:
        assert call_args == ['tar', '-xzvf', '/tmp/package.tar.gz', '--absolute-names', '--directory', '/some/directory',
                             '--strip-components=2', '--overwrite', 'some_target']

