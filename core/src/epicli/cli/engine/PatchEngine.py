import os

from cli.helpers.Config import Config
from cli.helpers.Log import Log
from cli.helpers.Step import Step

from cli.helpers.build_saver import get_build_path, get_inventory_path_for_build
from cli.helpers.build_saver import copy_files_recursively, copy_file
from cli.helpers.yaml_helpers import safe_load_all, dump
from cli.helpers.doc_list_helpers import select_single
from cli.helpers.argparse_helpers import components_to_dict

from cli.engine.schema.DefaultMerger import DefaultMerger
from cli.engine.schema.SchemaValidator import SchemaValidator

from cli.engine.ansible.AnsibleCommand import AnsibleCommand
from cli.engine.ansible.AnsibleRunner import AnsibleRunner


class PatchEngine(Step):
    """Perform backup and recovery operations."""

    def __init__(self, input_data):
        super().__init__(__name__)
        self.file = input_data.file
        self.parsed_components = None if input_data.components is None else set(input_data.components)
        self.component_dict = dict()
        self.input_docs = list()
        self.cluster_model = None
        self.backup_doc = None
        self.recovery_doc = None
        self.build_directory = None
        self.ansible_command = AnsibleCommand()

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def _process_input_docs(self):
        # Load the user input YAML docs from the input file
        if os.path.isabs(self.file):
            path_to_load = self.file
        else:
            path_to_load = os.path.join(os.getcwd(), self.file)
        user_file_stream = open(path_to_load, 'r')
        self.input_docs = safe_load_all(user_file_stream)

        # Merge the input docs with defaults
        with DefaultMerger(self.input_docs) as doc_merger:
            self.input_docs = doc_merger.run()

        # Get the cluster model
        self.cluster_model = select_single(self.input_docs, lambda x: x.kind == 'epiphany-cluster')
        if self.cluster_model is None:
            raise Exception('No cluster model defined in input YAML file')

        # Validate input documents
        with SchemaValidator(self.cluster_model, self.input_docs) as schema_validator:
            schema_validator.run()

        # Get backup config document
        self.backup_doc = select_single(self.input_docs, lambda x: x.kind == 'configuration/backup')

        # Get recovery config document
        self.recovery_doc = select_single(self.input_docs, lambda x: x.kind == 'configuration/recovery')

        # Derive the build directory path
        self.build_directory = get_build_path(self.cluster_model.specification.name)

    def _process_component_config(self, document):
        if self.parsed_components is not None:
            available_components = set(document.specification.components.keys())
            self.component_dict = components_to_dict(self.parsed_components, available_components)

    def backup(self):
        """Backup all enabled components."""

        self._process_input_docs()
        self._process_component_config(self.backup_doc)
        self._update_role_files_and_vars('backup', self.backup_doc)

        # Execute all enabled component playbooks sequentially
        for component_name, component_config in sorted(self.backup_doc.specification.components.items()):
            if self.component_dict:
                # Override yaml config with command line parameters
                if self.component_dict[component_name]:
                    self._update_playbook_files_and_run('backup', component_name)
            else:
                if component_config.enabled:
                    self._update_playbook_files_and_run('backup', component_name)

        return 0

    def recovery(self):
        """Recover all enabled components."""

        self._process_input_docs()
        self._process_component_config(self.recovery_doc)
        self._update_role_files_and_vars('recovery', self.recovery_doc)

        # Execute all enabled component playbooks sequentially
        for component_name, component_config in sorted(self.recovery_doc.specification.components.items()):
            if self.component_dict:
                # Override yaml config with command line parameters
                if self.component_dict[component_name]:
                    self._update_playbook_files_and_run('recovery', component_name)
            else:
                if component_config.enabled:
                    self._update_playbook_files_and_run('recovery', component_name)

        return 0

    def _update_role_files_and_vars(self, action, document):
        self.logger.info(f'Updating {action} role files...')

        # Copy role files
        roles_build_path = os.path.join(self.build_directory, 'ansible/roles', action)
        roles_source_path = os.path.join(AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH, 'roles', action)
        copy_files_recursively(roles_source_path, roles_build_path)

        # Render role vars
        vars_dir = os.path.join(roles_build_path, 'vars')
        os.makedirs(vars_dir, exist_ok=True)
        vars_file_path = os.path.join(vars_dir, 'main.yml')
        with open(vars_file_path, 'w') as stream:
            dump(document, stream)

    def _update_playbook_files_and_run(self, action, component):
        self.logger.info(f'Running {action} on {component}...')

        # Copy playbook file
        playbook_build_path = os.path.join(self.build_directory, 'ansible', f'{action}_{component}.yml')
        playbook_source_path = os.path.join(AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH, f'{action}_{component}.yml')
        copy_file(playbook_source_path, playbook_build_path)

        # Run the playbook
        inventory_path = get_inventory_path_for_build(self.build_directory)
        self.ansible_command.run_playbook(inventory=inventory_path, playbook_path=playbook_build_path)
