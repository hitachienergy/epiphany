import os
import subprocess
import shutil

from cli.helpers.Log import LogPipe, Log
from cli.helpers.Config import Config
from cli.helpers.data_loader import DATA_FOLDER_PATH


class SpecCommand:
    SPEC_TEST_PATH = DATA_FOLDER_PATH + '/common/tests'

    def __init__(self):
        self.logger = Log(__name__)

    def __init__(self):
        self.logger = Log(__name__)

    def check_dependencies(self):
        error_str = '''Missing Ruby or one of the following gems: serverspec, rake, rspec_junit_formatter. These need to be installed to run the cluster spec tests from epicli'''
        if  shutil.which('ruby') == None:
            raise Exception(error_str)

        if  shutil.which('gem') == None:
            raise Exception(error_str)

        #TODO: 'gem query --local' to check rake, rspec_junit_formatter

    def run(self, spec_output, inventory, user, key, group):
        self.check_dependencies()

        env = os.environ.copy()
        env['spec_output'] = spec_output
        env['inventory'] = inventory
        env['user'] = user
        env['keypath'] = key

        cmd = f'rake inventory="{inventory}" user={user} keypath="{key}" spec_output="{spec_output}" spec:{group}'

        self.logger.info(f'Running: "{cmd}"')

        logpipe = LogPipe(__name__)
        with subprocess.Popen(cmd.split(' '), cwd=self.SPEC_TEST_PATH, env=env, stdout=logpipe, stderr=logpipe, shell=True) as sp:
            logpipe.close()

        if sp.returncode != 0:
            raise Exception(f'Error running: "{cmd}"')
        else:
            self.logger.info(f'Done running: "{cmd}"')
