import os
import subprocess
from cli.helpers.Log import LogPipe, Log
import time


class AnsibleCommand:

    def __init__(self, working_directory=os.path.dirname(__file__)):
        self.logger = Log(__name__)
        self.working_directory = working_directory

    def __init__(self):
        self.logger = Log(__name__)

    def run_task(self, hosts, inventory, module, args):
        cmd = ['ansible']

        cmd.extend(["-m", module])

        if args is not None and len(args) > 0:
            cmd.extend(["-a", args])

        if inventory is not None and len(inventory) > 0:
            cmd.extend(["-i", inventory])

        cmd.append(hosts)

        self.logger.info('Running: "' + ' '.join(cmd) + '"')

        logpipe = LogPipe(__name__)
        with subprocess.Popen(cmd, stdout=logpipe, stderr=logpipe) as sp:
            logpipe.close()

        if sp.returncode != 0:
            raise Exception('Error running: "' + ' '.join(cmd) + '"')
        else:
            self.logger.info('Done running "' + ' '.join(cmd) + '"')

    def run_task_with_retries(self, inventory, module, args, hosts, retries, timeout=10):
        for i in range(retries):
            try:
                self.run_task(hosts=hosts, inventory=inventory, module=module,
                              args=args)
                break
            except Exception as e:
                self.logger.error(e)
                self.logger.info("Retry running task: " + str(i + 1) + "/" + str(retries))
                time.sleep(timeout)

    def run_playbook(self, inventory, playbook_path):
        cmd = ['ansible-playbook']

        if inventory is not None and len(inventory) > 0:
            cmd.extend(["-i", inventory])

        cmd.append(playbook_path)

        self.logger.info('Running: "' + ' '.join(cmd) + '"')

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
                return 0
            except Exception as e:
                self.logger.error(e)
                self.logger.info("Retry running playbook: " + str(i + 1) + "/" + str(retries))
                time.sleep(timeout)
        return 1
