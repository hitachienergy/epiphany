import os
import time

import ansible_runner

from cli.engine.AnsibleInventoryCreator import AnsibleInventoryCreator
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_inventory_path, get_ansible_path, copy_files_recursively


class AnsibleRunner(Step):
    ANSIBLE_PLAYBOOKS_PATH = "/../../../../core/src/ansible/"

    def __init__(self, cluster_model, config_docs):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.inventory_creator = AnsibleInventoryCreator(cluster_model, config_docs, use_public_ips=True)

    def __enter__(self):
        super().__enter__();
        self.inventory_creator.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback);
        self.inventory_creator.__exit__(exc_type, exc_value, traceback)

    def run(self):
        inventory_path = get_inventory_path(self.cluster_model.specification.name)

        for i in range(20):
            if_inventory_exists_and_have_content = os.path.exists(inventory_path) and os.path.getsize(
                inventory_path) > 0
            if if_inventory_exists_and_have_content:
                continue

            self.inventory_creator.create()
            time.sleep(10)

        src = os.path.dirname(__file__) + AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH

        copy_files_recursively(src, get_ansible_path(self.cluster_model.specification.name))

        # todo: install packages to run ansible on Red Hat hosts
        for i in range(10):
            runner = ansible_runner.run(private_data_dir=get_ansible_path(self.cluster_model.specification.name),
                                        host_pattern="all", inventory=inventory_path,
                                        module='raw', module_args='sudo apt-get install -y python-simplejson')
            print(runner.status)

            if runner.status.lower() == "successful":
                break

            time.sleep(10)

        for i in range(10):
            runner = ansible_runner.run(private_data_dir=get_ansible_path(self.cluster_model.specification.name),
                                        host_pattern="all", inventory=inventory_path,
                                        playbook=os.path.join(get_ansible_path(self.cluster_model.specification.name),
                                                              "common.yml"))
            print(runner.status)

            if runner.status.lower() == "successful":
                break

            time.sleep(10)

        # todo rename ansible playbooks
        for component in self.cluster_model.specification["components"]:
            print(component)

            runner = ansible_runner.run(private_data_dir=get_ansible_path(self.cluster_model.specification.name),
                                        host_pattern="all", inventory=inventory_path,
                                        playbook=os.path.join(get_ansible_path(self.cluster_model.specification.name),
                                                              component + ".yml"))

            print(runner.status)

            if runner.status.lower() == "successful":
                break

            time.sleep(10)
