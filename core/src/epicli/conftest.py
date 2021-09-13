from cli.helpers.Config import Config
import shutil
import os
from cli.helpers.build_saver import save_manifest, MANIFEST_FILE_NAME
from tests.helpers.constants import TEST_DOCS, CLUSTER_NAME_SAVE, CLUSTER_NAME_LOAD, NON_EXISTING_CLUSTER


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    Config().output_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'test_results/')
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
    shutil.rmtree(os.path.join(Config().output_dir, ), CLUSTER_NAME_LOAD)
    shutil.rmtree(os.path.join(Config().output_dir, ), CLUSTER_NAME_SAVE)
    shutil.rmtree(os.path.join(Config().output_dir, ), NON_EXISTING_CLUSTER)
    prepare_test_data_for_load()


def prepare_test_data_for_load():
    save_manifest(TEST_DOCS, CLUSTER_NAME_LOAD, MANIFEST_FILE_NAME)
