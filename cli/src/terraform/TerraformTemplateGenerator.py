from cli.src.helpers.build_io import (delete_files_matching_glob,
                                      get_terraform_path, save_terraform_file)
from cli.src.helpers.data_loader import load_template_file, template_types
from cli.src.Step import Step


class TerraformTemplateGenerator(Step):

    def __init__(self, cluster_model, infrastructure):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.infrastructure = [self.cluster_model] + infrastructure

    def run(self):
        terraform_output_dir = get_terraform_path(self.cluster_model.specification.name)

        # Only remove epicli generated .tf files, not tfstate or user created files.
        delete_files_matching_glob(terraform_output_dir, '[0-9][0-9][0-9]_*.tf')

        templates = filter(lambda x: x.kind != 'infrastructure/cloud-init-custom-data', self.infrastructure)
        for idx, doc in enumerate(templates):
            if doc.kind != 'epiphany-cluster':
                terraform_file_name = '{:03d}'.format(idx) + '_' + doc.specification.name + ".tf"
            else:
                terraform_file_name = '000_' + doc.specification.name + ".tf"

            self.logger.info('Generating: ' + doc.kind + ' ---> ' + terraform_file_name)

            template = load_template_file(template_types.TERRAFORM, doc.provider, doc.kind)
            content = template.render(doc)
            save_terraform_file(content, self.cluster_model.specification.name, terraform_file_name)
