from cli.engine.Terraform import Terraform
from cli.helpers.Step import Step


class TerraformRunner(Step):

    def __init__(self):
        super().__init__(__name__)
        self.terraform = Terraform()

    def run(self):
        self.terraform.init()
        self.terraform.apply(auto_approve=True)
