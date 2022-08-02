import subprocess
from unittest.mock import Mock, patch

import pytest
from src.command.debian.apt_cache import AptCache

from tests.data.apt_cache import APT_CACHE_DEPENDS_RABBITMQ_STDOUT, APT_CACHE_DEPENDS_SOLR_STDOUT
from tests.mocks.command_run_mock import CommandRunMock


def test_interface_get_package_dependencies(mocker):
    ''' Check argument construction for `apt-cache depends` '''
    with CommandRunMock(mocker, AptCache(1).get_package_dependencies, {'package': 'vim'}) as call_args:
        assert call_args == ['apt-cache',
                             'depends',
                             '--no-recommends',
                             '--no-suggests',
                             '--no-conflicts',
                             '--no-breaks',
                             '--no-replaces',
                             '--no-enhances',
                             '--no-pre-depends',
                             'vim']


APT_CACHE_DEPENDS_DATA = [
    ('tar', 'tar\n', []),
    ('rabbitmq-server', APT_CACHE_DEPENDS_RABBITMQ_STDOUT, ['adduser', 'erlang-base', 'erlang-crypto', 'python3']),
    ('solr-common', APT_CACHE_DEPENDS_SOLR_STDOUT, ['curl', 'debconf', 'default-jre-headless', 'libjs-jquery'])]

@pytest.mark.parametrize('PACKAGE_NAME, CMD_STDOUT, EXPECTED_DEPS', APT_CACHE_DEPENDS_DATA)
def test_get_package_dependencies_return_value(PACKAGE_NAME, CMD_STDOUT, EXPECTED_DEPS):
    mock_completed_proc = Mock(spec=subprocess.CompletedProcess)
    mock_completed_proc.returncode = 0
    mock_completed_proc.stdout = CMD_STDOUT

    with patch('src.command.command.subprocess.run') as mock_run:
        mock_run.return_value = mock_completed_proc
        return_value = AptCache(1).get_package_dependencies(package=PACKAGE_NAME)
        assert return_value == EXPECTED_DEPS
