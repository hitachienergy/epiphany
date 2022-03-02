import os

from cli.src.helpers.build_io import get_terraform_path
from cli.src.providers.provider_class_loader import provider_class_loader
from cli.src.Step import Step
from cli.src.terraform.TerraformCommand import TerraformCommand
from cli.src.terraform.TerraformFileCopier import TerraformFileCopier
from cli.src.terraform.TerraformTemplateGenerator import \
    TerraformTemplateGenerator


class TerraformRunner(Step):

    def __init__(self, cluster_model, infrastructure_docs=[]):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.infrastructure_docs = infrastructure_docs
        self.terraform = TerraformCommand(get_terraform_path(self.cluster_model.specification.name))
        self.new_env = os.environ.copy()
        apiproxy = provider_class_loader(self.cluster_model.provider, 'APIProxy')(self.cluster_model, [])
        apiproxy.login(self.new_env)

    def __enter__(self):
        super().__enter__()
        return self

    def run(self):
        pass

    def apply(self):
        # Generate terraform templates
        with TerraformTemplateGenerator(self.cluster_model, self.infrastructure_docs) as template_generator:
            template_generator.run()

        # Copy cloud-config.yml since it contains bash code which can't be templated easily (requires {% raw %}...{% endraw %})
        with TerraformFileCopier(self.cluster_model, self.infrastructure_docs) as file_copier:
            file_copier.run()

        # Run terraform apply
        self.terraform.init(env=self.new_env)
        self.terraform.apply(auto_approve=True, env=self.new_env)

    def destroy(self):
        self.terraform.destroy(auto_approve=True, env=self.new_env)
