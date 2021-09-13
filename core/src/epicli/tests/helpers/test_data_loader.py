import os
from cli.helpers.build_saver import get_build_path
from cli.helpers.data_loader import get_data_dir_path, get_provider_subdir_path, load_manifest_docs,\
    DATA_FOLDER_PATH
from tests.helpers.constants import TEST_DOCS

SCRIPT_DIR = "/workspaces/epiphany/core/src/epicli/data"
CLUSTER_NAME = 'test-load'

def test_get_data_dir_path():
    assert get_data_dir_path() == os.path.realpath(
        os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH))


def test_get_provider_subdir_path():
    assert get_provider_subdir_path("terraform", "aws") == os.path.realpath(
        os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH, "aws", "terraform"))

def test_load_manifest_docs():
    build_path = get_build_path(CLUSTER_NAME)
    docs = load_manifest_docs(build_path)
    assert docs == TEST_DOCS

