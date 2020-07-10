import os
import subprocess
from cli.helpers.Log import LogPipe, Log
from cli.helpers.Config import Config

terraform_verbosity = ['ERROR','WARN','INFO','DEBUG','TRACE']

class TerraformCommand:

    def __init__(self, working_directory=os.path.dirname(__file__)):
        self.logger = Log(__name__)
        self.APPLY_COMMAND = "apply"
        self.DESTROY_COMMAND = "destroy"
        self.PLAN_COMMAND = "plan"
        self.INIT_COMMAND = "init"
        self.working_directory = working_directory

    def apply(self, auto_approve=False, env=os.environ.copy()):
        self.run(self, self.APPLY_COMMAND, auto_approve=auto_approve, env=env, auto_retries=3)

    def destroy(self, auto_approve=False, env=os.environ.copy()):
        self.run(self, self.DESTROY_COMMAND, auto_approve=auto_approve, env=env)

    def plan(self, env=os.environ.copy()):
        self.run(self, self.PLAN_COMMAND, env=env)

    def init(self, env=os.environ.copy()):
        self.run(self, self.INIT_COMMAND, env=env)

    @staticmethod
    def run(self, command, env, auto_approve=False, auto_retries=1):
        cmd = ['terraform', command]

        if auto_approve:
            cmd.append('--auto-approve')

        if command == self.APPLY_COMMAND or command == self.DESTROY_COMMAND:
            cmd.append(f'-state={self.working_directory}/terraform.tfstate')

        cmd.append('-no-color')

        cmd.append(self.working_directory)

        cmd = ' '.join(cmd)
        self.logger.info(f'Running: "{cmd}"')

        if Config().debug > 0:
            env['TF_LOG'] = terraform_verbosity[Config().debug]

        retries = 1
        do_retry = True
        while ((retries <= auto_retries) and do_retry):
            logpipe = LogPipe(__name__)
            with subprocess.Popen(cmd, stdout=logpipe, stderr=logpipe, env=env,  shell=True) as sp:
                logpipe.close()
            retries = retries + 1
            do_retry = next((True for s in logpipe.stderrstrings if 'RetryableError' in s), False)
            if do_retry and retries <= auto_retries:
                self.logger.warning(f'Terraform failed with "RetryableError" error. Retry: ' + str(retries) + '/' + str(auto_retries))

        if sp.returncode != 0:
            raise Exception(f'Error running: "{cmd}"')
        else:
            self.logger.info(f'Done running "{cmd}"')
