import os

from cli.src.helpers.build_io import (ANSIBLE_INVENTORY_FILE, SPEC_OUTPUT_DIR,
                                      load_manifest)
from cli.src.helpers.doc_list_helpers import select_single
from cli.src.spec.SpecCommand import SpecCommand
from cli.src.Step import Step


class Test(Step):
    def __init__(self, input_data, available_test_groups: list[str]):
        super().__init__(__name__)
        self.build_directory = input_data.build_directory
        self.test_groups = input_data.included_groups

        if input_data.excluded_groups:
            included_groups = input_data.included_groups
            if 'all' in included_groups:
                included_groups = available_test_groups

            self.test_groups = sorted(set(included_groups) - set(input_data.excluded_groups))

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

        # run the spec tests
        spec_command = SpecCommand()
        if 'all' in self.test_groups:
            spec_command.run(spec_output, path_to_inventory, admin_user.name, admin_user.key_path, 'all')
        else:
            self.logger.info(f'Selected test groups: {self.test_groups}')
            for group in self.test_groups:
                spec_command.run(spec_output, path_to_inventory, admin_user.name, admin_user.key_path, group)

        return 0
