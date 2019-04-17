from cli.helpers.data_loader import load_template_file, types
from cli.helpers.build_saver import save_terraform_file
from cli.helpers.Step import Step


class TerraformTemplateGenerator(Step):

    def __init__(self, cluster_model, infrastructure):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.infrastructure = [cluster_model] + infrastructure

    def run(self):
        for idx, doc in enumerate(self.infrastructure):
            if doc.kind != 'epiphany-cluster':
                terraform_file_name = '{:03d}'.format(idx) + '_' + doc.specification.name + ".tf"
            else:
                terraform_file_name = '000_' + doc.specification.name + ".tf"

            self.logger.info('Generating: ' + doc.kind + ' ---> ' + terraform_file_name)

            template = load_template_file(types.TERRAFORM, doc.provider, doc.kind)
            content = template.render(doc)
            save_terraform_file(content, self.cluster_model.specification.name, terraform_file_name)












