import os
from pathlib import Path

from cli.helpers.Step import Step
from cli.helpers.build_io import copy_file, get_terraform_path, delete_files_matching_glob
from cli.helpers.data_loader import BASE_DIR, types


class TerraformFileCopier(Step):
    TERRAFORM_BASE_PATH = os.path.join(BASE_DIR, types.TERRAFORM)

    def __init__(self, cluster_model, infrastructure):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.infrastructure = [self.cluster_model] + infrastructure

    def run(self):
        terraform_output_dir = get_terraform_path(self.cluster_model.specification.name)
        # '*.yml' would remove cli.helpers.build_io.SP_FILE_NAME
        delete_files_matching_glob(terraform_output_dir, 'cloud-config.yml')

        files = filter(lambda x: x.kind == 'infrastructure/cloud-init-custom-data', self.infrastructure)
        for doc in files:
            if doc.specification.enabled:
                file_name = doc.specification.file_name
                src_path = Path(os.path.join(self.TERRAFORM_BASE_PATH, doc.provider)) / doc.kind / \
                    doc.specification.os_distribution / file_name
                if Path(src_path).is_file():
                    self.logger.info('Copying: ' + doc.kind + ' ---> ' + file_name)
                    dst_path = Path(terraform_output_dir) / file_name
                    copy_file(src_path, dst_path)
