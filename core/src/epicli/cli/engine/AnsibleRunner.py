from cli.engine.AnsibleInventoryCreator import AnsibleInventoryCreator
from cli.engine.Step import Step


class AnsibleRunner(Step):
    def __init__(self, cluster_model, config_docs):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.inventory_creator = AnsibleInventoryCreator(cluster_model, config_docs)

    def __enter__(self):
        super().__enter__();
        self.inventory_creator.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback);
        self.inventory_creator.__exit__(exc_type, exc_value, traceback)

    def run(self):
        inventory = self.inventory_creator.create()
        # todo run ansible playbooks



