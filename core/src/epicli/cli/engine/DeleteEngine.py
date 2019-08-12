import os
import shutil

from cli.helpers.Step import Step
from cli.helpers.Config import Config
from cli.helpers.build_saver import MANIFEST_FILE_NAME, TERRAFORM_OUTPUT_DIR
from cli.helpers.data_loader import load_yamls_file
from cli.helpers.doc_list_helpers import select_single
from cli.engine.terraform.TerraformRunner import TerraformRunner

class DeleteEngine(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.build_directory = input_data.build_directory

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def delete(self):
        try:
            path_to_manifest = os.path.join(self.build_directory, MANIFEST_FILE_NAME)
            if not os.path.isfile(path_to_manifest):
                raise Exception('No manifest.yml inside the build folder')

            docs = load_yamls_file(path_to_manifest)
            cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
            
            if cluster_model.provider == 'any':
                raise Exception('Delete works only for cloud providers')
 
            with TerraformRunner(cluster_model, docs) as tf_runner:
                tf_runner.delete()     
                
            shutil.rmtree(self.build_directory, ignore_errors=True)     

            return 0
        except Exception as e:
            self.logger.error(e, exc_info=True)  # TODO extensive debug output might not always be wanted. Make this configurable with input flag?
            return 1