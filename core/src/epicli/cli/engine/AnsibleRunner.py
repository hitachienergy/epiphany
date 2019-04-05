import os
import time

import ansible_runner

from cli.engine.AnsibleInventoryCreator import AnsibleInventoryCreator
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_inventory_path, get_output_path


class AnsibleRunner(Step):
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
            if_inventory_exists_and_have_content = os.path.exists(inventory_path) and os.path.getsize(inventory_path) > 0
            if if_inventory_exists_and_have_content:
                continue

            inventory = self.inventory_creator.create()
            time.sleep(10)

        # todo run ansible playbooks
        for i in range(30):
            runner = ansible_runner.run(private_data_dir=get_output_path(), host_pattern="all",
                                        inventory=inventory_path,
                                        module='shell', module_args='whoami')
            if runner.status == "successful":
                continue

            time.sleep(10)
