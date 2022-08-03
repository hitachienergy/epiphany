from copy import deepcopy  # make sure that objects used in tests don't get damaged in between test cases
from pathlib import Path

import pytest

from library.filter_credentials import _get_filtered_manifest

from library.tests.data.filter_credentials_data import (
    CLUSTER_DOC_ANY,
    CLUSTER_DOC_AWS,
    CLUSTER_DOC_AZURE,
    EXPECTED_CLUSTER_DOC_ANY,
    EXPECTED_CLUSTER_DOC_AWS,
    EXPECTED_CLUSTER_DOC_AZURE,
    MANIFEST_WITH_ADDITIONAL_DOCS
)


@pytest.mark.parametrize('CLUSTER_DOC, EXPECTED_OUTPUT_DOC',
                         [(CLUSTER_DOC_ANY, EXPECTED_CLUSTER_DOC_ANY),
                          (CLUSTER_DOC_AZURE, EXPECTED_CLUSTER_DOC_AZURE),
                          (CLUSTER_DOC_AWS, EXPECTED_CLUSTER_DOC_AWS)])
def test_epiphany_cluster_doc_filtering(CLUSTER_DOC, EXPECTED_OUTPUT_DOC, mocker):
    # Ignore yaml parsing, work on python objects:
    mocker.patch('library.filter_credentials.yaml.safe_load_all', return_value=[deepcopy(CLUSTER_DOC)])
    mocker.patch('library.filter_credentials.yaml.dump_all', side_effect=lambda docs: docs)
    mocker.patch('library.filter_credentials.Path.open')

    assert _get_filtered_manifest(Path('')) == [EXPECTED_OUTPUT_DOC]


def test_not_needed_docs_filtering(mocker):
    # Ignore yaml parsing, work on python objects:
    mocker.patch('library.filter_credentials.yaml.safe_load_all', return_value=deepcopy(MANIFEST_WITH_ADDITIONAL_DOCS))
    mocker.patch('library.filter_credentials.yaml.dump_all', side_effect=lambda docs: docs)
    mocker.patch('library.filter_credentials.Path.open')

    EXPECTED_DOCS = ['epiphany-cluster', 'configuration/feature-mappings', 'configuration/image-registry']
    FILTERED_DOCS = [doc['kind'] for doc in _get_filtered_manifest(Path(''))]

    assert FILTERED_DOCS == EXPECTED_DOCS
