import logging
from pathlib import Path

import yaml

from src.config.config import Config
from tests.data.config import EXPECTED_VERBOSE_OUTPUT
from tests.data.manifest_reader import INPUT_MANIFEST_ROLES_MAPPING


def test_manifest_verbose_output(mocker, caplog):
    ''' Check output produced when running download-requirements script with the `-v|--verbose` flag and with provided `-m|--manifest` '''

    mocker.patch('src.config.manifest_reader.load_yaml_file_all', return_value=yaml.safe_load_all(INPUT_MANIFEST_ROLES_MAPPING))
    caplog.set_level(logging.INFO)

    # mock Config's init methods:
    Config._Config__add_args = lambda *args: None
    Config._Config__log_info_summary = lambda *args: None

    config = Config([])

    # mock required config data:
    config.dest_manifest = Path('/some/path')
    config.verbose_mode = True
    config.read_manifest({})

    log_output = f'\n{"".join(caplog.messages)}\n'

    assert log_output == EXPECTED_VERBOSE_OUTPUT
