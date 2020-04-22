import os
import subprocess
import shutil
from subprocess import Popen, PIPE

from cli.helpers.Log import LogPipe, Log
from cli.helpers.Config import Config
from cli.helpers.data_loader import DATA_FOLDER_PATH

SPEC_TEST_PATH = DATA_FOLDER_PATH + '/common/tests'

class SpecCommand:
    def __init__(self):
        self.logger = Log(__name__)


    def __init__(self):
        self.logger = Log(__name__)


    def check_dependencies(self):
        required_gems = ['serverspec', 'rake', 'rspec_junit_formatter'] 

        error_str = f'''Missing Ruby or one of the following Ruby gems: {', '.join(required_gems)}
These need to be installed to run the cluster spec tests from epicli'''

        if  shutil.which('ruby') == None or shutil.which('gem') == None:
            raise Exception(error_str)

        p = subprocess.Popen(['gem', 'query', '--local'], stdout=PIPE)
        out, err = p.communicate()
        if all(n in out.decode('utf-8') for n in required_gems) == False: 
            raise Exception(error_str)


    def run(self, spec_output, inventory, user, key, group):
        self.check_dependencies()

        env = os.environ.copy()
        env['spec_output'] = spec_output
        env['inventory'] = inventory
        env['user'] = user
        env['keypath'] = key

        cmd = f'rake inventory={inventory} user={user} keypath={key} spec_output={spec_output} spec:{group}'

        self.logger.info(f'Running: "{cmd}"')

        logpipe = LogPipe(__name__)
        with Popen(cmd.split(' '), cwd=SPEC_TEST_PATH, env=env, stdout=logpipe, stderr=logpipe) as sp:
            logpipe.close()

        if sp.returncode != 0:
            raise Exception(f'Error running: "{cmd}"')
        else:
            self.logger.info(f'Done running: "{cmd}"')


    @staticmethod
    def get_spec_groups():
        groups = os.listdir(SPEC_TEST_PATH + '/spec')
        groups.remove('spec_helper.rb')
        groups = ['all'] + groups
        sorted(groups, key=str.lower)
        return groups