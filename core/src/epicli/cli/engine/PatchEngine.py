import os

from cli.engine.AnsibleCommand import AnsibleCommand
from cli.engine.AnsibleRunner import AnsibleRunner
from cli.helpers.Config import Config
from cli.helpers.Step import Step
from cli.helpers.build_saver import copy_files_recursively, copy_file, get_inventory_path_for_build


class PatchEngine(Step):

    def __init__(self):
        super().__init__(__name__)
        self.ansible_command = AnsibleCommand()

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def run(self):
        pass

    def run_upgrade(self):
        try:
            build_directory = Config().output_dir
            build_roles_directory = os.path.join(build_directory, 'ansible/roles')

            upgrade_playbook_path = os.path.join(build_roles_directory, 'upgrade')
            backup_playbook_path = os.path.join(build_roles_directory, 'backup')
            recovery_playbook_path = os.path.join(build_roles_directory, 'recovery')

            upgrade_role_path = os.path.join(build_directory, 'ansible', 'upgrade.yml')

            epiphany_playbooks_path = os.path.dirname(__file__) + AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH
            epiphany_roles_path = os.path.join(epiphany_playbooks_path, 'roles')

            upgrade_role_source_path = os.path.join(epiphany_roles_path, 'upgrade')
            backup_role_source_path = os.path.join(epiphany_roles_path, 'backup')
            restore_role_source_path = os.path.join(epiphany_roles_path, 'recovery')
            playbook_source_path = os.path.join(epiphany_playbooks_path, 'upgrade.yml')

            copy_files_recursively(upgrade_role_source_path, upgrade_playbook_path)
            copy_files_recursively(backup_role_source_path, backup_playbook_path)
            copy_files_recursively(restore_role_source_path, recovery_playbook_path)
            copy_file(playbook_source_path, upgrade_role_path)

            inventory_path = get_inventory_path_for_build(build_directory)
            self.ansible_command.run_playbook(inventory=inventory_path, playbook_path=upgrade_role_path)
            return 0
        except Exception as e:
            self.logger.error(e, exc_info=True)  # TODO extensive debug output might not always be wanted. Make this configurable with input flag?
            return 1

    def run_backup(self):
        try:
            build_directory = Config().output_dir
            backup_role_path = os.path.join(build_directory, 'ansible', 'backup.yml')
            inventory_path = get_inventory_path_for_build(build_directory)
            self.ansible_command.run_playbook(inventory=inventory_path, playbook_path=backup_role_path)

            return 0
        except Exception as e:
            self.logger.error(e, exc_info=True)  # TODO extensive debug output might not always be wanted. Make this configurable with input flag?
            return 1

    def run_recovery(self):
        try:
            build_directory = Config().output_dir
            backup_role_path = os.path.join(build_directory, 'ansible', 'recovery.yml')
            inventory_path = get_inventory_path_for_build(build_directory)
            self.ansible_command.run_playbook(inventory=inventory_path, playbook_path=backup_role_path)

            return 0
        except Exception as e:
            self.logger.error(e, exc_info=True)  # TODO extensive debug output might not always be wanted. Make this configurable with input flag?
            return 1