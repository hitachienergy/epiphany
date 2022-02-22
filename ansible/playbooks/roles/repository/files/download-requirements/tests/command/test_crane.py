from pathlib import Path
from tests.mocks.command_run_mock import CommandRunMock

from src.command.crane import Crane


def test_interface_pull(mocker):
    ''' Check argument construction for crane pull '''
    mocker.patch('src.command.crane.chmod', return_value=None)
    mocker.patch('src.command.crane.mkstemp', return_value=[None, '/tmp/tmpfile'])
    mocker.patch('src.command.crane.move', return_value=None)

    with CommandRunMock(mocker, Crane(1).pull, {'image_name': 'image',
                                                'destination': Path('/some/place'),
                                                'platform': 'platform',
                                                'legacy_format': True,
                                                'insecure': True}) as call_args:
        assert call_args == ['crane', 'pull', '--insecure', '--platform=platform', '--format=legacy',
                             'image', '/tmp/tmpfile']
