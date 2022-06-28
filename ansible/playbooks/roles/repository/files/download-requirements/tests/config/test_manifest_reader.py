from pathlib import Path

import pytest
import yaml

from src.config.manifest_reader import ManifestReader
from src.config.os_type import OSArch
from tests.data.manifest_reader import (EXPECTED_FEATURE_MAPPINGS,
                                        EXPECTED_FEATURE_MAPPINGS_WITH_DASHBOARDS,
                                        EXPECTED_FEATURE_MAPPINGS_WITH_IMAGES_ARM64,
                                        EXPECTED_FEATURE_MAPPINGS_WITH_IMAGES_X86_64,
                                        INPUT_MANIFEST_FEATURE_MAPPINGS,
                                        INPUT_MANIFEST_WITH_DASHBOARDS,
                                        INPUT_MANIFEST_WITH_IMAGES)

@pytest.mark.parametrize('INPUT_DOC, EXPECTED_OUTPUT_DOC, OS_ARCH',
                         [(INPUT_MANIFEST_FEATURE_MAPPINGS, EXPECTED_FEATURE_MAPPINGS, OSArch.X86_64),
                          (INPUT_MANIFEST_WITH_DASHBOARDS, EXPECTED_FEATURE_MAPPINGS_WITH_DASHBOARDS, OSArch.X86_64),
                          (INPUT_MANIFEST_WITH_IMAGES, EXPECTED_FEATURE_MAPPINGS_WITH_IMAGES_X86_64, OSArch.X86_64),
                          (INPUT_MANIFEST_WITH_IMAGES, EXPECTED_FEATURE_MAPPINGS_WITH_IMAGES_ARM64, OSArch.ARM64)])
def test_parse_manifest(INPUT_DOC, EXPECTED_OUTPUT_DOC, OS_ARCH, mocker):
    ''' Check manifest file parsing '''
    mocker.patch('src.config.manifest_reader.load_yaml_file_all', return_value=yaml.safe_load_all(INPUT_DOC))

    mreader = ManifestReader(Path('/some/path'), OS_ARCH)
    assert mreader.parse_manifest() == EXPECTED_OUTPUT_DOC
