import os
import time

from cli.src.ansible.AnsibleCommand import AnsibleCommand
from cli.src.ansible.AnsibleConfigFileCreator import AnsibleConfigFileCreator
from cli.src.ansible.AnsibleInventoryCreator import AnsibleInventoryCreator
from cli.src.ansible.AnsibleInventoryUpgrade import AnsibleInventoryUpgrade
from cli.src.ansible.AnsibleVarsGenerator import AnsibleVarsGenerator
from cli.src.Config import Config
from cli.src.helpers.build_io import (copy_files_recursively, delete_directory,
                                      get_ansible_config_file_path,
                                      get_ansible_config_file_path_for_build,
                                      get_ansible_path,
                                      get_ansible_path_for_build,
                                      get_inventory_path,
                                      get_inventory_path_for_build)
from cli.src.helpers.data_loader import ANSIBLE_PLAYBOOK_PATH
from cli.src.helpers.naming_helpers import to_role_name
from cli.src.Step import Step


class AnsibleRunner(Step):
    def __init__(self, cluster_model=None, config_docs=None, build_dir=None, backup_build_dir=None,
                 ansible_options=None, ping_retries: int = 5):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.build_dir = build_dir
        self.backup_build_dir = backup_build_dir
        self.ansible_options = ansible_options
        self.ansible_command = AnsibleCommand()
        self.ping_retries: int = ping_retries

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def playbook_path(self, name):
        if self.cluster_model != None:
            return os.path.join(get_ansible_path(self.cluster_model.specification.name), f'{name}.yml')
        else:
            return os.path.join(get_ansible_path_for_build(self.build_dir), f'{name}.yml')

    def copy_resources(self):
        self.logger.info('Copying Ansible resources')
        if self.cluster_model != None:
            ansible_dir = get_ansible_path(self.cluster_model.specification.name)
        else:
            ansible_dir = get_ansible_path_for_build(self.build_dir)

        delete_directory(ansible_dir)
        copy_files_recursively(ANSIBLE_PLAYBOOK_PATH, ansible_dir)

    def pre_flight(self, inventory_path):
        self.logger.info('Checking connection to each machine')
        self.ansible_command.run_task_with_retries(inventory=inventory_path,
                                                   module="ping",
                                                   hosts="all",
                                                   retries=self.ping_retries)

        self.logger.info('Checking preflight conditions on each machine')
        self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                       playbook_path=self.playbook_path('preflight'),
                                                       retries=1)

        self.logger.info('Setting up repository for cluster provisioning. This will take a while...')
        self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                       playbook_path=self.playbook_path('repository_setup'),
                                                       retries=1)

        self.ansible_command.run_playbook(inventory=inventory_path,
                                          playbook_path=self.playbook_path('common'))

    def post_flight(self, inventory_path):
        self.ansible_command.run_playbook(inventory=inventory_path,
                                          playbook_path=self.playbook_path('repository_teardown'))

        self.ansible_command.run_playbook(inventory=inventory_path,
                                          playbook_path=self.playbook_path('postflight'))

    def apply(self):
        inventory_path = get_inventory_path(self.cluster_model.specification.name)

        # copy resources
        self.copy_resources()

        # create inventory
        inventory_creator = AnsibleInventoryCreator(self.cluster_model, self.config_docs)
        inventory_creator.create()

        # create ansible.cfg
        ansible_config_file_path = get_ansible_config_file_path(self.cluster_model.specification.name)
        ansible_cfg_creator = AnsibleConfigFileCreator(self.ansible_options, ansible_config_file_path)
        ansible_cfg_creator.create()

        # generate vars
        ansible_vars_generator = AnsibleVarsGenerator(inventory_creator=inventory_creator)
        ansible_vars_generator.generate()

        # pre-flight to prepare machines
        self.pre_flight(inventory_path)

        # run roles
        enabled_roles = inventory_creator.get_enabled_roles()
        for role in enabled_roles:
            self.ansible_command.run_playbook(inventory=inventory_path,
                                              playbook_path=self.playbook_path(to_role_name(role)), vault_file=Config().vault_password_location)

        #post-flight after we are done
        self.post_flight(inventory_path)

    def upgrade(self):
        inventory_path = get_inventory_path_for_build(self.build_dir)

        # copy resources
        self.copy_resources()

        # upgrade inventory
        inventory_upgrade = AnsibleInventoryUpgrade(self.build_dir, self.backup_build_dir, self.config_docs)
        inventory_upgrade.upgrade()

        # create ansible.cfg
        ansible_config_file_path = get_ansible_config_file_path_for_build(self.build_dir)
        ansible_cfg_creator = AnsibleConfigFileCreator(self.ansible_options, ansible_config_file_path)
        ansible_cfg_creator.create()

        # generate vars
        ansible_vars_generator = AnsibleVarsGenerator(inventory_upgrade=inventory_upgrade)
        ansible_vars_generator.generate()

        # pre-flight to prepare machines
        self.pre_flight(inventory_path)

        # run image_registry playbook
        self.ansible_command.run_playbook(inventory=inventory_path,
                                          playbook_path=self.playbook_path('image_registry'))

        # run upgrade playbook
        self.ansible_command.run_playbook(inventory=inventory_path,
                                          playbook_path=self.playbook_path('upgrade'))

        #post-flight after we are done
        self.post_flight(inventory_path)
