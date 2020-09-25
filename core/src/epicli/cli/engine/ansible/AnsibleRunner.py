import inspect
import os
import time
import shutil
from os.path import dirname

from cli.engine.ansible.AnsibleCommand import AnsibleCommand
from cli.engine.ansible.AnsibleInventoryCreator import AnsibleInventoryCreator
from cli.engine.ansible.AnsibleConfigFileCreator import AnsibleConfigFileCreator
from cli.engine.ansible.AnsibleVarsGenerator import AnsibleVarsGenerator
from cli.engine.ansible.AnsibleInventoryUpgrade import AnsibleInventoryUpgrade
from cli.helpers.Step import Step
from cli.helpers.build_saver import (get_inventory_path, get_inventory_path_for_build,
    get_ansible_path, get_ansible_path_for_build, get_ansible_config_file_path, get_ansible_config_file_path_for_build,
    copy_files_recursively)
from cli.helpers.naming_helpers import to_role_name
from cli.helpers.data_loader import DATA_FOLDER_PATH
from cli.helpers.Config import Config


class AnsibleRunner(Step):
    ANSIBLE_PLAYBOOKS_PATH = DATA_FOLDER_PATH + '/common/ansible/playbooks/'

    def __init__(self, cluster_model=None, config_docs=None, build_dir=None, backup_build_dir=None,
                 ansible_options=None):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.build_dir = build_dir
        self.backup_build_dir = backup_build_dir
        self.ansible_options = ansible_options
        self.ansible_command = AnsibleCommand()

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

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

        shutil.rmtree(ansible_dir, ignore_errors=True)
        copy_files_recursively(AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH, ansible_dir)

        # copy skopeo so Ansible can move it to the repositry machine
        if not Config().offline_requirements:
            shutil.copy(os.path.join(dirname(dirname(inspect.getfile(os))), 'skopeo_linux'), '/tmp')

    def pre_flight(self, inventory_path):
        self.logger.info('Checking connection to each machine')
        self.ansible_command.run_task_with_retries(inventory=inventory_path,
                                                   module="ping",
                                                   hosts="all",
                                                   retries=5)

        self.logger.info('Checking preflight conditions on each machine')
        self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                       playbook_path=self.playbook_path('preflight'),
                                                       retries=1)

        self.logger.info('Setting up SSH tunnel for kubectl')
        self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                       playbook_path=self.playbook_path('sshtunnel_setup_k8s'),
                                                       retries=1)

        self.logger.info('Setting up SSH tunnel for helm')
        self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                       playbook_path=self.playbook_path('sshtunnel_setup_helm'),
                                                       retries=1)

        self.logger.info('Setting up repository for cluster provisioning. This will take a while...')
        self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                       playbook_path=self.playbook_path('repository_setup'),
                                                       retries=1)

        self.ansible_command.run_playbook(inventory=inventory_path,
                                          playbook_path=self.playbook_path('common'))

    def post_flight(self, inventory_path):
        self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                       playbook_path=self.playbook_path('sshtunnel_teardown_k8s'),
                                                       retries=1)

        self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                       playbook_path=self.playbook_path('sshtunnel_teardown_helm'),
                                                       retries=1)

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
        time.sleep(10)

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
        inventory_upgrade = AnsibleInventoryUpgrade(self.build_dir, self.backup_build_dir)
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
