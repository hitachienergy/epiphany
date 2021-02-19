from cli.helpers.Step import Step
from cli.helpers.build_saver import copy_file, get_terraform_path, remove_files_matching_glob
from cli.helpers.data_loader import types, get_provider_subdir_path
from pathlib import Path


class TerraformFileCopier(Step):

    def __init__(self, cluster_model, infrastructure):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.infrastructure = [self.cluster_model] + infrastructure

    def run(self):
        terraform_output_dir = get_terraform_path(self.cluster_model.specification.name)
        # '*.yml' would remove cli.helpers.build_saver.SP_FILE_NAME
        remove_files_matching_glob(terraform_output_dir, 'cloud-config.yml')

        files = filter(lambda x: x.kind == 'infrastructure/cloud-init-custom-data', self.infrastructure)
        for doc in files:
            if doc.specification.enabled:
                file_name = doc.specification.file_name
                src_path = Path(get_provider_subdir_path(types.TERRAFORM, doc.provider)) / doc.kind / \
                    doc.specification.os_distribution / file_name
                if Path(src_path).is_file():
                    self.logger.info('Copying: ' + doc.kind + ' ---> ' + file_name)
                    dst_path = Path(terraform_output_dir) / file_name
                    copy_file(src_path, dst_path)
