import os
import time

from cli.engine.AnsibleInventoryCreator import AnsibleInventoryCreator
from cli.helpers.build_saver import get_inventory_path


class AnsibleRunner:
    def __init__(self, cluster_model, config_docs):
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.inventory_creator = AnsibleInventoryCreator(cluster_model, config_docs)

    def __enter__(self):
        self.inventory_creator.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
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
