from config import template_generator_config
from helpers import terraform_file_helper
from modules.template_generator import TemplateGenerator
from modules.terraform_runner.Terraform import Terraform


class TerraformRunner:

    def __init__(self, terraform_build_directory, cluster_model, infrastructure):
        self.terraform_build_directory = terraform_build_directory
        self.terraform = Terraform(terraform_build_directory)
        self.template_generator = TemplateGenerator.TemplateGenerator()
        self.template_generator_config = template_generator_config
        self.cluster_model = [cluster_model]
        self.infrastructure = infrastructure

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        terraform_file_helper.create_terraform_output_dir(self.terraform_build_directory)
        terraform_file_helper.generate_terraform_file(self.cluster_model, self.template_generator,
                                                      self.template_generator_config, self.terraform_build_directory)

        terraform_file_helper.generate_terraform_file(self.infrastructure, self.template_generator,
                                                      self.template_generator_config, self.terraform_build_directory)

        self.terraform.init()
        self.terraform.apply(auto_approve=True)
