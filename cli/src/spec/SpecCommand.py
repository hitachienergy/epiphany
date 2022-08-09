import os
import shutil
import subprocess
from pathlib import Path
from subprocess import PIPE, Popen

from cli.src.Config import Config
from cli.src.helpers.data_loader import BASE_DIR
from cli.src.Log import Log, LogPipe

SPEC_TESTS_PATH = Path(BASE_DIR).resolve() / 'tests' / 'spec'

class SpecCommand:
    def __init__(self):
        self.logger = Log(__name__)


    def check_dependencies(self):
        required_gems = ['serverspec', 'rake', 'rspec_junit_formatter']

        error_str = f'''Missing Ruby or one of the following Ruby gems: {', '.join(required_gems)}
These need to be installed to run the cluster spec tests from epicli'''

        if  shutil.which('ruby') is None or shutil.which('gem') is None:
            raise Exception(error_str)

        p = subprocess.Popen(['gem', 'list', '--local'], stdout=PIPE)
        out, err = p.communicate()
        if all(n in out.decode('utf-8') for n in required_gems) is False:
            raise Exception(error_str)


    def run(self, spec_output, inventory, user, key, groups):
        self.check_dependencies()

        env = os.environ.copy()
        env['spec_output'] = spec_output
        env['inventory'] = inventory
        env['user'] = user
        env['keypath'] = key

        if not Config().no_color:
            env['rspec_extra_opts'] = '--force-color'

        cmd = f'rake inventory={inventory} user={user} keypath={key} spec_output={spec_output} spec:{" spec:".join(groups)}'

        self.logger.info(f'Running: "{cmd}"')

        logpipe = LogPipe(__name__)
        with Popen(cmd.split(' '), cwd=SPEC_TESTS_PATH, env=env, stdout=logpipe, stderr=logpipe) as sp:
            logpipe.close()

        if sp.returncode != 0:
            raise Exception(f'Error running: "{cmd}"')
        else:
            self.logger.info(f'Done running: "{cmd}"')


    @staticmethod
    def get_spec_groups() -> list[str]:
        """Get test groups based on directories."""
        groups_path = SPEC_TESTS_PATH / 'spec'
        groups = [str(item.name) for item in groups_path.iterdir() if item.is_dir()]

        return sorted(groups)
