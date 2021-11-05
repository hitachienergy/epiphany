import os
import subprocess
import time

from cli.helpers.Log import LogPipe, Log
from cli.helpers.Config import Config


ansible_verbosity = ['NONE','-v','-vv','-vvv','-vvvv']

class AnsibleCommand:

    def __init__(self, working_directory=os.path.dirname(__file__)):
        self.logger = Log(__name__)
        self.working_directory = working_directory


    def run_task(self, hosts, inventory, module, args=None):
        cmd = ['ansible']

        cmd.extend(["-m", module])

        if args is not None and len(args) > 0:
            cmd.extend(["-a", args])

        if inventory is not None and len(inventory) > 0:
            cmd.extend(["-i", inventory])

        cmd.append(hosts)

        if Config().debug > 0:
            cmd.append(ansible_verbosity[Config().debug])

        self.logger.info('Running: "' + ' '.join(module) + '"')

        logpipe = LogPipe(__name__)
        with subprocess.Popen(cmd, stdout=logpipe, stderr=logpipe) as sp:
            logpipe.close()

        if sp.returncode != 0:
            raise Exception('Error running: "' + ' '.join(cmd) + '"')
        else:
            self.logger.info('Done running "' + ' '.join(cmd) + '"')

    def run_task_with_retries(self, inventory, module, hosts, retries, timeout=10, args=None):
        for i in range(retries):
            try:
                self.run_task(hosts=hosts, inventory=inventory, module=module,
                              args=args)
                break
            except Exception as e:
                self.logger.error(e)
                self.logger.warning('Retry running task: ' + str(i + 1) + '/' + str(retries))
                time.sleep(timeout)
        else:
            raise Exception(f'Failed running task after {str(retries)} retries')

    def run_playbook(self, inventory, playbook_path, vault_file=None, extra_vars=None):
        cmd = ['ansible-playbook']

        if inventory is not None and len(inventory) > 0:
            cmd.extend(['-i', inventory])

        if vault_file is not None:
            cmd.extend(['--vault-password-file', vault_file])

        if extra_vars is not None:
            variables = ' '.join([f"{variable}='{value}'" for variable, value in extra_vars.items()])
            cmd.extend(['--extra-vars', variables])

        cmd.append(playbook_path)

        if Config().debug > 0:
            cmd.append(ansible_verbosity[Config().debug])

        self.logger.info('Running: "' + ' '.join(playbook_path) + '"')

        logpipe = LogPipe(__name__)
        with subprocess.Popen(cmd, stdout=logpipe, stderr=logpipe) as sp:
            logpipe.close()

        if sp.returncode != 0:
            raise Exception('Error running: "' + ' '.join(cmd) + '"')
        else:
            self.logger.info('Done running "' + ' '.join(cmd) + '"')

    def run_playbook_with_retries(self, inventory, playbook_path, retries, timeout=10):
        for i in range(retries):
            try:
                self.run_playbook(inventory=inventory,
                                  playbook_path=playbook_path)
                break
            except Exception as e:
                self.logger.error(e)
                self.logger.warning('Retry running playbook: ' + str(i + 1) + '/' + str(retries))
                time.sleep(timeout)
        else:
            raise Exception(f'Failed running playbook after {str(retries)} retries')
