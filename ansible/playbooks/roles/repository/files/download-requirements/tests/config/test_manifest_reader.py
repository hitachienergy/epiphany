from pathlib import Path

import pytest
import yaml

from src.config.manifest_reader import ManifestReader
from tests.data.manifest_reader import (EXPECTED_FEATURE_MAPPINGS,
                                        EXPECTED_FEATURE_MAPPINGS_WITH_DASHBOARDS,
                                        INPUT_MANIFEST_FEATURE_MAPPINGS,
                                        INPUT_MANIFEST_WITH_DASHBOARDS)

@pytest.mark.parametrize('INPUT_DOC, EXPECTED_OUTPUT_DOC',
                         [(INPUT_MANIFEST_FEATURE_MAPPINGS, EXPECTED_FEATURE_MAPPINGS),
                          (INPUT_MANIFEST_WITH_DASHBOARDS, EXPECTED_FEATURE_MAPPINGS_WITH_DASHBOARDS)])
def test_parse_manifest(INPUT_DOC, EXPECTED_OUTPUT_DOC, mocker):
    ''' Check manifest file parsing '''
    mocker.patch('src.config.manifest_reader.load_yaml_file_all', return_value=yaml.safe_load_all(INPUT_DOC))

    mreader = ManifestReader(Path('/some/path'))
    assert mreader.parse_manifest() == EXPECTED_OUTPUT_DOC
