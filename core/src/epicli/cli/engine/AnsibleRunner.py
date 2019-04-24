import os
import time

from cli.engine.AnsibleCommand import AnsibleCommand
from cli.engine.AnsibleInventoryCreator import AnsibleInventoryCreator
from cli.engine.AnsibleVarsGenerator import AnsibleVarsGenerator
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_inventory_path, get_ansible_path, copy_files_recursively
from cli.helpers.role_name_helper import adjust_name


class AnsibleRunner(Step):
    ANSIBLE_PLAYBOOKS_PATH = "/../../data/common/ansible/playbooks/"

    def __init__(self, cluster_model, config_docs):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.inventory_creator = AnsibleInventoryCreator(cluster_model, config_docs, use_public_ips=True)
        self.ansible_command = AnsibleCommand()
        self.ansible_vars_generator = AnsibleVarsGenerator(cluster_model, config_docs)

    def __enter__(self):
        super().__enter__()
        self.inventory_creator.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        self.inventory_creator.__exit__(exc_type, exc_value, traceback)

    def run(self):
        inventory_path = get_inventory_path(self.cluster_model.specification.name)

        for i in range(20):
            if_inventory_exists_and_have_content = os.path.exists(inventory_path) and os.path.getsize(
                inventory_path) > 0
            if if_inventory_exists_and_have_content:
                break

            self.inventory_creator.create()
            time.sleep(10)

        src = os.path.dirname(__file__) + AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH

        copy_files_recursively(src, get_ansible_path(self.cluster_model.specification.name))

        # todo: install packages to run ansible on Red Hat hosts
        self.ansible_command.run_task_with_retries(hosts="all", inventory=inventory_path, module="raw",
                                                   args="sudo apt-get install -y python-simplejson", retries=5)

        self.ansible_vars_generator.run()

        self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
                                                       playbook_path=os.path.join(
                                                           get_ansible_path(self.cluster_model.specification.name),
                                                           "common.yml"), retries=5)

        # todo: run commented playbooks
        # for component in self.cluster_model.specification["components"]:
        #
        #     roles = self.inventory_creator.get_roles_for_feature(component_key=component)
        #
        #     for role in roles:
        #         self.ansible_command.run_playbook_with_retries(inventory=inventory_path,
        #                                                        playbook_path=os.path.join(
        #                                                            get_ansible_path(
        #                                                                self.cluster_model.specification.name),
        #                                                            adjust_name(role) + ".yml"), retries=5)
