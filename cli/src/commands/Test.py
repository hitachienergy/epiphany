import os

from cli.src.ansible.AnsibleCommand import AnsibleCommand
from cli.src.helpers.build_io import (SPEC_OUTPUT_DIR,
                                      get_inventory_path_for_build, load_inventory, load_manifest)
from cli.src.helpers.doc_list_helpers import select_single
from cli.src.spec.SpecCommand import SPEC_TESTS_PATH, SpecCommand
from cli.src.Step import Step


class Test(Step):
    def __init__(self, input_data, test_groups):
        super().__init__(__name__)
        self.build_directory = input_data.build_directory
        self.inventory_path = get_inventory_path_for_build(self.build_directory)
        self.excluded_groups = input_data.excluded_groups
        self.included_groups = input_data.included_groups
        self.kubeconfig_remote_path = input_data.kubeconfig_remote_path
        self.all_groups = test_groups
        self.available_groups = self.__get_available_test_groups()
        self.selected_groups = self.__get_selected_test_groups()
        self.ansible_command = None

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __get_inventory_groups(self, append_implicit: bool) -> list[str]:
        inventory_groups = load_inventory(self.inventory_path).list_groups()
        if append_implicit:
            inventory_groups.append('common')
        return inventory_groups

    def __get_available_test_groups(self) -> list[str]:
        inventory_groups = self.__get_inventory_groups(True)
        return [group for group in self.all_groups if group in inventory_groups]


    def __get_selected_test_groups(self) -> list[str]:
        selected_groups = self.included_groups

        if 'all' in selected_groups:
            selected_groups = ['all']

        # exclude test groups
        if self.excluded_groups:
            included_groups = self.included_groups
            if 'all' in included_groups:
                included_groups = self.available_groups

            selected_groups = [group for group in included_groups if group not in self.excluded_groups]

        return selected_groups

    def __is_env_preparation_needed(self) -> bool:
        if self.kubeconfig_remote_path:
            kubectl_groups = ['applications', 'kubernetes_master']
            if any(group in kubectl_groups for group in self.selected_groups):
                return True
            if 'all' in self.selected_groups and any(group in kubectl_groups for group in self.available_groups):
                return True

        return False

    def __prepare_env(self):
        if self.__is_env_preparation_needed():
            self.ansible_command = AnsibleCommand()
            playbook_path = str(SPEC_TESTS_PATH) + '/pre_run/ansible/kubernetes_master/copy-kubeconfig.yml'
            self.ansible_command.run_playbook(inventory=self.inventory_path,
                                              playbook_path=playbook_path,
                                              extra_vars=[f'kubeconfig_remote_path={self.kubeconfig_remote_path}'])

    def __clean_up_env(self):
        if self.__is_env_preparation_needed():
            playbook_path = str(SPEC_TESTS_PATH) + '/post_run/ansible/kubernetes_master/undo-copy-kubeconfig.yml'
            self.ansible_command.run_playbook(inventory=self.inventory_path,
                                              playbook_path=playbook_path)

    def test(self):
        # get manifest documents
        docs = load_manifest(self.build_directory)
        cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')

        # get admin user
        admin_user = cluster_model.specification.admin_user
        if not os.path.isfile(admin_user.key_path):
            raise Exception(f'No SSH key file in directory: "{admin_user.key_path}"')

        # get and create the spec output dir if it does not exist
        spec_output = os.path.join(self.build_directory, SPEC_OUTPUT_DIR)
        if not os.path.exists(spec_output):
            os.makedirs(spec_output)

        # run the spec tests
        if self.selected_groups:
            self.__prepare_env()
            spec_command = SpecCommand()

            if 'all' not in self.selected_groups:
                self.logger.info(f'Selected test groups: {", ".join(self.selected_groups)}')

            spec_command.run(spec_output, self.inventory_path, admin_user.name, admin_user.key_path, self.selected_groups)
            self.__clean_up_env()
        else:
            raise Exception('No test group specified to run')

        return 0
