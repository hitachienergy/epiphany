import os

from cli.helpers.Step import Step
from cli.engine.ansible.AnsibleCommand import AnsibleCommand
from cli.engine.ansible.AnsibleRunner import AnsibleRunner
from cli.helpers.Config import Config
from cli.helpers.build_saver import copy_files_recursively, copy_file, get_inventory_path_for_build


class PatchEngine(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.build_directory = input_data.build_directory
        self.ansible_command = AnsibleCommand()

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def upgrade(self):
        self.upgrade_patch_files_and_run('upgrade')
        return 0

    def backup(self):
        self.upgrade_patch_files_and_run('backup')
        return 0

    def recovery(self):
        self.upgrade_patch_files_and_run('recovery')
        return 0

    def upgrade_patch_files_and_run(self, action):
        self.logger.info(f'Running {action}...')

        #copy role files
        roles_build_path = os.path.join(self.build_directory, 'ansible/roles', action)
        roles_source_path = os.path.join(AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH, 'roles', action)
        copy_files_recursively(roles_source_path, roles_build_path)

        #copy playbook file
        playbook_build_path = os.path.join(self.build_directory, 'ansible/') + action + '.yml'
        playbook_source_path = os.path.join(AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH) + action + '.yml' 
        copy_file(playbook_source_path, playbook_build_path)  
        
        #run the playbook
        inventory_path = get_inventory_path_for_build(self.build_directory)
        self.ansible_command.run_playbook(inventory=inventory_path, playbook_path=playbook_build_path)        