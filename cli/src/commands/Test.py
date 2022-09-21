import os
from pathlib import Path

from cli.src.Step import Step
from cli.src.ansible.AnsibleCommand import AnsibleCommand
from cli.src.helpers.build_io import SPEC_OUTPUT_DIR, get_inventory_path_for_build, load_inventory
from cli.src.schema.ManifestHandler import ManifestHandler
from cli.src.spec.SpecCommand import SPEC_TESTS_PATH, SpecCommand


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

    def __get_inventory_groups(self, append_implicit: bool) -> list[str]:
        """
        Get list of groups from Ansible inventory

        :param append_implicit: if True, `common` group, which is not present in inventory, is appended
        """
        inventory_groups = load_inventory(self.inventory_path).list_groups()
        if append_implicit:
            inventory_groups.append('common')
        return inventory_groups

    def __get_available_test_groups(self) -> list[str]:
        """
        Get list of all test groups that can be run
        """
        inventory_groups = self.__get_inventory_groups(True)
        return [group for group in self.all_groups if group in inventory_groups]

    def __get_selected_test_groups(self) -> list[str]:
        """
        Get list of test groups selected to be run
        """
        selected_groups = ['all'] if 'all' in self.included_groups else self.included_groups

        # exclude test groups
        if self.excluded_groups:
            included_groups = self.available_groups if 'all' in self.included_groups else self.included_groups
            selected_groups = [group for group in included_groups if group not in self.excluded_groups]

        return selected_groups

    def __is_env_preparation_needed(self) -> bool:
        """
        Check whether additional actions are needed in order to run selected test groups
        """
        if self.kubeconfig_remote_path:
            kubectl_groups = ('applications', 'keycloak', 'kubernetes_master')
            if any(group in kubectl_groups for group in self.selected_groups):
                return True
            if 'all' in self.selected_groups and any(group in kubectl_groups for group in self.available_groups):
                return True

        return False

    def __prepare_env(self):
        if self.__is_env_preparation_needed():
            playbook_path = str(SPEC_TESTS_PATH) + '/pre_run/ansible/kubernetes_master/copy-kubeconfig.yml'
            ansible_command = AnsibleCommand()
            ansible_command.run_playbook(inventory=self.inventory_path,
                                         playbook_path=playbook_path,
                                         extra_vars=[f'kubeconfig_remote_path={self.kubeconfig_remote_path}'])

    def __clean_up_env(self):
        if self.__is_env_preparation_needed():
            playbook_path = str(SPEC_TESTS_PATH) + '/post_run/ansible/kubernetes_master/undo-copy-kubeconfig.yml'
            ansible_command = AnsibleCommand()
            ansible_command.run_playbook(inventory=self.inventory_path, playbook_path=playbook_path)

    def test(self):
        """
        Run spec tests for selected groups
        """
        if not self.selected_groups:
            raise Exception('No test group specified to run')

        # get manifest documents
        mhandler = ManifestHandler(build_path=Path(self.build_directory))
        mhandler.read_manifest()
        cluster_model = mhandler.cluster_model

        # get admin user
        admin_user = cluster_model.specification.admin_user
        if not os.path.isfile(admin_user.key_path):
            raise Exception(f'No SSH key file in directory: "{admin_user.key_path}"')

        # get and create the spec output dir if it does not exist
        spec_output = os.path.join(self.build_directory, SPEC_OUTPUT_DIR)
        if not os.path.exists(spec_output):
            os.makedirs(spec_output)

        if 'all' not in self.selected_groups:
            self.logger.info(f'Selected test groups: {", ".join(self.selected_groups)}')

        self.__prepare_env()

        # run tests
        spec_command = SpecCommand()
        spec_command.run(spec_output, self.inventory_path, admin_user.name, admin_user.key_path, self.selected_groups)

        self.__clean_up_env()

        return 0
