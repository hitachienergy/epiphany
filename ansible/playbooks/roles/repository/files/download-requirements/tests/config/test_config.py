from pathlib import Path
import logging

import pytest
import yaml

from src.config.config import Config
from tests.data.config import (DASHBOARD_REQUIREMENTS,
                               EXPECTED_VERBOSE_OUTPUT,
                               EXPECTED_VERBOSE_DASHBOARD_OUTPUT,
                               EXPECTED_VERBOSE_FILE_OUTPUT,
                               FILE_REQUIREMENTS)
from tests.data.manifest_reader import (INPUT_MANIFEST_FEATURE_MAPPINGS,
                                        INPUT_MANIFEST_WITH_DASHBOARDS)


@pytest.fixture(scope='class')
def default_manifest(request):
    """
    Generate default requirements for each test
    """
    request.cls.MANIFEST = {
        'files': '',
        'grafana-dashboards': ''
    }


@pytest.mark.usefixtures('default_manifest')
class TestConfig:
    @pytest.mark.parametrize('INPUT_DOC, EXPECTED_OUTPUT_DOC, REQUIREMENTS',
                             [(INPUT_MANIFEST_FEATURE_MAPPINGS, EXPECTED_VERBOSE_OUTPUT, DASHBOARD_REQUIREMENTS),
                              (INPUT_MANIFEST_WITH_DASHBOARDS, EXPECTED_VERBOSE_DASHBOARD_OUTPUT, DASHBOARD_REQUIREMENTS),
                              (INPUT_MANIFEST_FEATURE_MAPPINGS, EXPECTED_VERBOSE_FILE_OUTPUT, FILE_REQUIREMENTS)
                             ])
    def test_manifest_verbose_output(self, INPUT_DOC: str,
                                     EXPECTED_OUTPUT_DOC: str,
                                     REQUIREMENTS: str,
                                     mocker, caplog):
        """
        Check output produced when running download-requirements script with the `-v|--verbose` flag and with provided `-m|--manifest`

        :param INPUT_DOC: yaml doc which will be parsed by the ManifestReader
        :param EXPECTED_OUTPUT_DOC: expected output to be printed by the `Config` class, then tested against the parsed `INPUT_DOC`
        :param REQUIREMENTS: yaml doc containing requirements passed to `Config`'s read_manifest()
        """

        mocker.patch('src.config.manifest_reader.load_yaml_file_all', return_value=yaml.safe_load_all(INPUT_DOC))
        caplog.set_level(logging.INFO)

        # mock Config's init methods:
        Config._Config__add_args = lambda *args: None
        Config._Config__log_info_summary = lambda *args: None

        config = Config([])

        # mock required config data:
        config.dest_manifest = Path('/some/path')
        config.verbose_mode = True

        req_key, doc = tuple(yaml.safe_load(REQUIREMENTS).items())[0]

        self.MANIFEST[req_key] = doc
        config.read_manifest(self.MANIFEST)

        log_output = f'\n{"".join(caplog.messages)}\n'

        assert log_output == EXPECTED_OUTPUT_DOC
