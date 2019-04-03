from cli.engine.Terraform import Terraform
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_terraform_path

class TerraformRunner(Step):

    def __init__(self, cluster_model):
        super().__init__(__name__)
        self.terraform = Terraform(get_terraform_path(cluster_model.specification.name))

    def run(self):
        self.terraform.init()
        self.terraform.apply(auto_approve=True)
