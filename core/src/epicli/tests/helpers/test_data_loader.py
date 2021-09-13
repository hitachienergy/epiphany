import os
import pytest
from cli.helpers.build_saver import get_build_path
from cli.helpers.data_loader import get_data_dir_path, get_provider_subdir_path, load_manifest_docs,\
    DATA_FOLDER_PATH
from tests.helpers.constants import CLUSTER_NAME_LOAD, TEST_DOCS

SCRIPT_DIR = "/workspaces/epiphany/core/src/epicli/data"

def test_get_data_dir_path():
    assert get_data_dir_path() == os.path.realpath(
        os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH))


def test_get_provider_subdir_path():
    assert get_provider_subdir_path("terraform", "aws") == os.path.realpath(
        os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH, "aws", "terraform"))

def test_load_manifest_docs():
    build_path = get_build_path(CLUSTER_NAME_LOAD)
    docs = load_manifest_docs(build_path)
    assert docs == TEST_DOCS

def test_load_not_existing_manifest_docs():
    build_path = get_build_path(CLUSTER_NAME_LOAD + "aaaa")
    with pytest.raises(Exception):
        load_manifest_docs(build_path)
