import os

from cli.src.helpers.build_io import (ANSIBLE_INVENTORY_FILE, SPEC_OUTPUT_DIR,
                                      load_manifest)
from cli.src.helpers.build_io import load_inventory
from cli.src.helpers.doc_list_helpers import select_single
from cli.src.spec.SpecCommand import SpecCommand
from cli.src.Step import Step


class Test(Step):
    def __init__(self, input_data, test_groups):
        super().__init__(__name__)
        self.build_directory = input_data.build_directory
        self.excluded_groups = input_data.excluded_groups
        self.included_groups = input_data.included_groups
        self.test_groups = test_groups

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def test(self):
        # get manifest documents
        docs = load_manifest(self.build_directory)
        cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')

        # get inventory
        path_to_inventory = os.path.join(self.build_directory, ANSIBLE_INVENTORY_FILE)
        if not os.path.isfile(path_to_inventory):
            raise Exception(f'No "{ANSIBLE_INVENTORY_FILE}" inside the build directory: "{self.build_directory}"')

        # get admin user
        admin_user = cluster_model.specification.admin_user
        if not os.path.isfile(admin_user.key_path):
            raise Exception(f'No SSH key file in directory: "{admin_user.key_path}"')

        # get and create the spec output dir if it does not exist
        spec_output = os.path.join(self.build_directory, SPEC_OUTPUT_DIR)
        if not os.path.exists(spec_output):
            os.makedirs(spec_output)

        selected_test_groups = self.included_groups

        # exclude test groups
        if self.excluded_groups:
            included_groups = self.included_groups
            if 'all' in included_groups:
                # get available test groups
                inventory_groups = load_inventory(path_to_inventory).list_groups()
                effective_inventory_groups = inventory_groups + ['common']
                included_groups = [group for group in self.test_groups if group in effective_inventory_groups]

            selected_test_groups = [group for group in included_groups if group not in self.excluded_groups]

        # run the spec tests
        if selected_test_groups:
            spec_command = SpecCommand()
            if 'all' in selected_test_groups:
                selected_test_groups = ['all']
            else:
                self.logger.info(f'Selected test groups: {", ".join(selected_test_groups)}')

            spec_command.run(spec_output, path_to_inventory, admin_user.name, admin_user.key_path, selected_test_groups)
        else:
            raise Exception('No test group specified to run')

        return 0
