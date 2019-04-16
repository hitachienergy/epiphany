from cli.engine.TerraformCommand import TerraformCommand
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_terraform_path


class TerraformRunner(Step):

    def __init__(self, cluster_model):
        super().__init__(__name__)
        self.terraform = TerraformCommand(get_terraform_path(cluster_model.specification.name))

    def __enter__(self):
        super().__enter__()
        self.terraform.check()
        return self

    def run(self):
        self.terraform.init()
        self.terraform.apply(auto_approve=True)

