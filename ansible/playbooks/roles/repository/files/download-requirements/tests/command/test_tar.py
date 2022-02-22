from tests.mocks.command_run_mock import CommandRunMock

from src.command.tar import Tar


def test_interface_pack(mocker):
    ''' Check argument construction for `tar -cf` '''
    with CommandRunMock(mocker, Tar().pack, {'filename': '/tmp/package.tar.gz',
                                             'target': '*',
                                             'directory': '/some/directory',
                                             'verbose': True,
                                             'compress': True,
                                             'verify': True}) as call_args:
        assert call_args == ['tar', '-czvf', '/tmp/package.tar.gz', '--verify', '--directory', '/some/directory', '*']


def test_interface_unpack(mocker):
    ''' Check argument construction for `tar -xf` '''
    with CommandRunMock(mocker, Tar().unpack, {'filename': '/tmp/package.tar.gz',
                                               'target': 'some_target',
                                               'absolute_names': True,
                                               'directory': '/some/directory',
                                               'overwrite': True,
                                               'verbose': True,
                                               'uncompress': True,
                                               'strip_components': 2}) as call_args:
        assert call_args == ['tar', '-xzvf', '/tmp/package.tar.gz', '--absolute-names', '--directory', '/some/directory',
                             '--strip-components=2', 'some_target', '--overwrite']

