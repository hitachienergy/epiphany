import os
import shutil

from cli.helpers.Step import Step
from cli.helpers.Config import Config
from cli.helpers.build_saver import SPEC_OUTPUT_DIR, ANSIBLE_OUTPUT_DIR, INVENTORY_FILE_NAME
from cli.helpers.data_loader import load_yamls_file
from cli.helpers.doc_list_helpers import select_single
from cli.engine.spec.SpecCommand import SpecCommand
from cli.helpers.data_loader import load_manifest_docs

class TestEngine(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.build_directory = input_data.build_directory
        self.group = input_data.group

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def test(self):
        # get manifest documents
        docs = load_manifest_docs(self.build_directory)
        cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')

        # get inventory
        path_to_inventory = os.path.join(self.build_directory, INVENTORY_FILE_NAME)
        if not os.path.isfile(path_to_inventory):
            raise Exception(f'No "{INVENTORY_FILE_NAME}" inside the build directory: "{self.build_directory}"')        

        # get admin user
        admin_user = cluster_model.specification.admin_user
        if not os.path.isfile(admin_user.key_path):
            raise Exception(f'No SSH key file in directory: "{admin_user.key_path}"')

        # get and create the spec output dir if it does not exist
        spec_output = os.path.join(self.build_directory, SPEC_OUTPUT_DIR)
        if not os.path.exists(spec_output):
            os.makedirs(spec_output)
        
        # run the spec tests
        spec_command = SpecCommand()
        spec_command.run(spec_output, path_to_inventory, admin_user.name, admin_user.key_path, self.group)   

        return 0
