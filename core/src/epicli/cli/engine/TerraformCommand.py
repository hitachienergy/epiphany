import os
import subprocess
from cli.helpers.Log import LogPipe, Log


class TerraformCommand:

    def __init__(self, working_directory=os.path.dirname(__file__)):
        self.logger = Log(__name__)
        self.APPLY_COMMAND = "apply"
        self.DESTROY_COMMAND = "destroy"
        self.PLAN_COMMAND = "plan"
        self.INIT_COMMAND = "init"
        self.working_directory = working_directory

    def apply(self, auto_approve=False):
        self.run(self, self.APPLY_COMMAND, auto_approve=auto_approve)

    def destroy(self, auto_approve=False):
        self.run(self, self.DESTROY_COMMAND, auto_approve=auto_approve)

    def plan(self):
        self.run(self, self.PLAN_COMMAND)

    def init(self):
        self.run(self, self.INIT_COMMAND)

    @staticmethod
    def run(self, command, auto_approve=False):
        cmd = ['terraform', command]

        if auto_approve:
            cmd.append('--auto-approve')

        if command == self.APPLY_COMMAND:
            cmd.append('-state=' + self.working_directory + '/terraform.tfstate')

        cmd.append(self.working_directory)

        self.logger.info('Running: "' + ' '.join(cmd) + '"')

        logpipe = LogPipe(__name__)
        with subprocess.Popen(cmd, stdout=logpipe, stderr=logpipe) as sp:
            logpipe.close()

        if sp.returncode != 0:
            raise Exception('Error running: "' + ' '.join(cmd) + '"')
        else:
            self.logger.info('Done running "' + ' '.join(cmd) + '"')
