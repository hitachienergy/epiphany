import inspect
import os
import time
import shutil
from os.path import dirname

from cli.engine.ansible.AnsibleCommand import AnsibleCommand
from cli.engine.ansible.AnsibleInventoryCreator import AnsibleInventoryCreator
from cli.engine.ansible.AnsibleVarsGenerator import AnsibleVarsGenerator
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_inventory_path, get_ansible_path, copy_files_recursively
from cli.helpers.naming_helpers import to_role_name
from cli.helpers.data_loader import DATA_FOLDER_PATH
from cli.helpers.Config import Config


class AnsibleRunner(Step):
    ANSIBLE_PLAYBOOKS_PATH = DATA_FOLDER_PATH + '/common/ansible/playbooks/'

    def __init__(self, cluster_model, config_docs):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.inventory_creator = AnsibleInventoryCreator(cluster_model, config_docs)
        self.ansible_command = AnsibleCommand()
        self.ansible_vars_generator = AnsibleVarsGenerator(cluster_model, config_docs, self.inventory_creator)

    def __enter__(self):
        super().__enter__()
        self.inventory_creator.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        self.inventory_creator.__exit__(exc_type, exc_value, traceback)

    def playbook_path(self, name):
        return os.path.join(get_ansible_path(self.cluster_model.specification.name), f'{name}.yml')       

    def run(self):
        inventory_path = get_inventory_path(self.cluster_model.specification.name)

        # create inventory on every run
        self.inventory_creator.create()
        time.sleep(10)

        copy_files_recursively(AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH, get_ansible_path(self.cluster_model.specification.name))

        # copy skopeo so Ansible can move it to the repositry machine
        if not Config().offline_requirements:
            shutil.copy(os.path.join(dirname(dirname(inspect.getfile(os))), 'skopeo_linux'), '/tmp')

        # todo: install packages to run ansible on Red Hat hosts
        self.ansible_command.run_task_with_retries(hosts='all', inventory=inventory_path, module='raw',
                                                   args='cat /etc/lsb-release | grep -i DISTRIB_ID | grep -i ubuntu && '
                                                        'sudo apt-get update && sudo apt-get install -y python-simplejson '
                                                        '|| echo \'Cannot find information about Ubuntu distribution\'', retries=5)

        self.ansible_vars_generator.run()

        self.logger.info('Setting up repository for cluster provisioning. This will take a while...')
        repository_setup_play_result = self.ansible_command.run_playbook_with_retries(
                                                                            inventory=inventory_path,
                                                                            playbook_path=self.playbook_path('repository-setup'),
                                                                            retries=5)

        if repository_setup_play_result != 0:
            return

        common_play_result = self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                                            playbook_path=self.playbook_path('common'),
                                                                            retries=1)
        if common_play_result != 0:
            return

        enabled_roles = self.inventory_creator.get_enabled_roles()

        for role in enabled_roles:
            play_result = self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                                         playbook_path=self.playbook_path(to_role_name(role)),
                                                                         retries=1)
            if play_result != 0:
                break

        repository_teardown_play_result = self.ansible_command.run_playbook_with_retries(
                                                                            inventory=inventory_path,
                                                                            playbook_path=self.playbook_path('repository-teardown'),
                                                                            retries=1)

        if repository_teardown_play_result != 0:
            return
