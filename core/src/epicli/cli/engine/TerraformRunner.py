from config import template_generator_config
from helpers import terraform_file_helper
from cli.engine import TemplateGenerator
from cli.engine.Terraform import Terraform
from cli.engine.Step import Step


class TerraformRunner(Step):

    def __init__(self, terraform_build_directory, cluster_model, infrastructure):
        super().__init__(__name__)
        self.terraform_build_directory = terraform_build_directory
        self.terraform = Terraform(terraform_build_directory)
        self.template_generator = TemplateGenerator.TemplateGenerator()
        self.template_generator_config = template_generator_config
        self.cluster_model = [cluster_model]
        self.infrastructure = infrastructure

    def run(self):
        terraform_file_helper.create_terraform_output_dir(self.terraform_build_directory)
        terraform_file_helper.generate_terraform_file(self.cluster_model, self.template_generator,
                                                      self.template_generator_config, self.terraform_build_directory)

        terraform_file_helper.generate_terraform_file(self.infrastructure, self.template_generator,
                                                      self.template_generator_config, self.terraform_build_directory)

        self.terraform.init()
        self.terraform.apply(auto_approve=True)
