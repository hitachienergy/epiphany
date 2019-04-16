import os
import subprocess
from cli.helpers.Log import LogPipe, Log
import time


class AnsibleCommand:

    def __init__(self, working_directory=os.path.dirname(__file__)):
        self.logger = Log.get_logger(__name__)
        self.working_directory = working_directory

    def __init__(self):
        self.logger = Log.get_logger(__name__)

    def check(self):
        try:
            # todo add terraform version check?
            output = subprocess.check_output(['ansible', '--version'])
            self.logger.info(output.decode().split('\n')[0])
        except subprocess.CalledProcessError as e:
            raise Exception('Ansible does not seem to be installed')

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
                self.logger.error("There was exception running module: " + module + " with parameters: " + args +
                                  ". Will retry 5 times. Retry: " + str(i + 1))
                self.logger.error(e)
                time.sleep(timeout)

    def run_playbook(self, inventory, playbook_path):
        cmd = ['ansible-playbook']

        self.logger.info('Running: "' + ' '.join(cmd) + '"')

        if inventory is not None and len(inventory) > 0:
            cmd.extend(["-i", inventory])

        cmd.append(playbook_path)

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
                self.logger.error("There was exception running ansible playbook: " + playbook_path +
                                  ". Will retry 5 times. Retry: " + str(i + 1))
                self.logger.error(e)
                time.sleep(timeout)
