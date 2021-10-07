import json
import os
import shutil

from cli.helpers.build_io import save_manifest, MANIFEST_FILE_NAME
from cli.helpers.Config import Config
from tests.unit.helpers.constants import TEST_DOCS, CLUSTER_NAME_SAVE, CLUSTER_NAME_LOAD, NON_EXISTING_CLUSTER,\
    TEST_JSON, TEST_JSON_NAME

def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    Config().output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_results/')
    prepare_test_directory()


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """

def prepare_test_directory():
    for path in [CLUSTER_NAME_LOAD, CLUSTER_NAME_SAVE, NON_EXISTING_CLUSTER, TEST_JSON_NAME]:
        rm_existing(os.path.join(Config().output_dir, path))
    prepare_test_data_for_load()


def prepare_test_data_for_load():
    save_manifest(TEST_DOCS, CLUSTER_NAME_LOAD, MANIFEST_FILE_NAME)
    with open(os.path.join(Config().output_dir, TEST_JSON_NAME), 'w') as out:
        json.dump(TEST_JSON, out)

def rm_existing(path):
    if os.path.exists(path):
        shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
