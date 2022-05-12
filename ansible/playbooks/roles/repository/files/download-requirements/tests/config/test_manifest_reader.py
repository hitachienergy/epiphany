from pathlib import Path

import yaml

from src.config.manifest_reader import ManifestReader
from tests.data.manifest_reader import EXPECTED_FEATURE_MAPPINGS, INPUT_MANIFEST_FEATURE_MAPPINGS

def test_parse_manifest(mocker):
    ''' Check manifest file parsing '''
    mocker.patch('src.config.manifest_reader.load_yaml_file_all', return_value=yaml.safe_load_all(INPUT_MANIFEST_FEATURE_MAPPINGS))

    mreader = ManifestReader(Path('/some/path'))
    assert mreader.parse_manifest() == EXPECTED_FEATURE_MAPPINGS
