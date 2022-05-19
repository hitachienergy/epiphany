import logging
from pathlib import Path

import pytest
import yaml

from src.config.config import Config
from tests.data.config import EXPECTED_VERBOSE_OUTPUT, EXPECTED_VERBOSE_DASHBOARD_OUTPUT, DASHBOARD_REQUIREMENTS
from tests.data.manifest_reader import INPUT_MANIFEST_FEATURE_MAPPINGS, INPUT_MANIFEST_WITH_DASHBOARDS


@pytest.mark.parametrize('INPUT_DOC, EXPECTED_OUTPUT_DOC',
                         [(INPUT_MANIFEST_FEATURE_MAPPINGS, EXPECTED_VERBOSE_OUTPUT),
                          (INPUT_MANIFEST_WITH_DASHBOARDS, EXPECTED_VERBOSE_DASHBOARD_OUTPUT)])
def test_manifest_verbose_output(INPUT_DOC, EXPECTED_OUTPUT_DOC, mocker, caplog):
    ''' Check output produced when running download-requirements script with the `-v|--verbose` flag and with provided `-m|--manifest` '''

    mocker.patch('src.config.manifest_reader.load_yaml_file_all', return_value=yaml.safe_load_all(INPUT_DOC))
    caplog.set_level(logging.INFO)

    # mock Config's init methods:
    Config._Config__add_args = lambda *args: None
    Config._Config__log_info_summary = lambda *args: None

    config = Config([])

    # mock required config data:
    config.dest_manifest = Path('/some/path')
    config.verbose_mode = True
    config.read_manifest(yaml.safe_load(DASHBOARD_REQUIREMENTS))

    log_output = f'\n{"".join(caplog.messages)}\n'

    assert log_output == EXPECTED_OUTPUT_DOC
