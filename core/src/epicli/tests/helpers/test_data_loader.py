import os
from cli.helpers.data_loader import get_data_dir_path, get_provider_subdir_path,\
    DATA_FOLDER_PATH

SCRIPT_DIR = "/workspaces/epiphany/core/src/epicli/data"


def test_get_data_dir_path():
    assert get_data_dir_path() == os.path.realpath(
        os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH))


def test_get_provider_subdir_path():
    assert get_provider_subdir_path("terraform", "aws") == os.path.realpath(
        os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH, "aws", "terraform"))
