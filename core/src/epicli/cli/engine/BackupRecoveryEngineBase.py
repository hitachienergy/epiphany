import os
import copy
import jsonschema

from cli.version import VERSION
from cli.helpers.Step import Step

from cli.helpers.build_saver import get_inventory_path_for_build
from cli.helpers.build_saver import copy_files_recursively, copy_file
from cli.helpers.build_saver import MANIFEST_FILE_NAME

from cli.helpers.yaml_helpers import dump
from cli.helpers.data_loader import load_yamls_file, load_yaml_obj, types as data_types
from cli.helpers.doc_list_helpers import select_single, ExpectedSingleResultException

from cli.engine.schema.DefaultMerger import DefaultMerger
from cli.engine.ansible.AnsibleCommand import AnsibleCommand
from cli.engine.ansible.AnsibleRunner import AnsibleRunner


class BackupRecoveryEngineBase(Step):
    """Perform backup and recovery operations (abstract base class)."""

    def __init__(self, input_data):
        # super(BackupRecoveryEngineBase, self).__init__(__name__) needs to be called in any subclass
        self.file = input_data.file
        self.build_directory = input_data.build_directory
        self.manifest_docs = list()
        self.input_docs = list()
        self.configuration_docs = list()
        self.cluster_model = None
        self.backup_doc = None
        self.recovery_doc = None
        self.ansible_command = AnsibleCommand()

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def _validate_input_doc(self, document):
        # Load document schema
        schema = load_yaml_obj(data_types.VALIDATION, self.cluster_model.provider, document.kind)

        # Include standard "definitions"
        schema['definitions'] = load_yaml_obj(data_types.VALIDATION, self.cluster_model.provider, 'core/definitions')

        # Assert the schema
        jsonschema.validate(instance=document, schema=schema)

    def _process_input_docs(self):
        """Load, validate and merge (with defaults) input yaml documents."""

        path_to_manifest = os.path.join(self.build_directory, MANIFEST_FILE_NAME)
        if not os.path.isfile(path_to_manifest):
            raise Exception('No manifest.yml inside the build folder')

        # Get existing manifest config documents
        self.manifest_docs = load_yamls_file(path_to_manifest)
        self.cluster_model = select_single(self.manifest_docs, lambda x: x.kind == 'epiphany-cluster')

        # Load backup / recovery configuration documents
        self.input_docs = load_yamls_file(self.file)

        # Validate all input documents
        for document in self.input_docs:
            self._validate_input_doc(document)

        # Merge the input docs with defaults
        with DefaultMerger(self.input_docs) as doc_merger:
            self.input_docs = doc_merger.run()

    def _process_configuration_docs(self):
        """Populate input yaml documents with additional required ad-hoc data."""

        # Seed the self.configuration_docs
        self.configuration_docs = copy.deepcopy(self.input_docs)

        # Please notice using DefaultMerger is not needed here, since it is done already at this point.
        # We just check if documents are missing and insert default ones without the unneeded merge operation.
        for kind in {'configuration/backup', 'configuration/recovery'}:
            try:
                # Check if the required document is in user inputs
                document = select_single(self.configuration_docs, lambda x: x.kind == kind)
            except ExpectedSingleResultException:
                # If there is no document provided by the user, then fallback to defaults
                document = load_yaml_obj(data_types.DEFAULT, 'common', kind)
                # Inject the required "version" attribute
                document['version'] = VERSION
                # Copy the "provider" value from the cluster model
                document['provider'] = self.cluster_model.provider
                # Save the document for later use
                self.configuration_docs.append(document)
            finally:
                # Copy the "provider" value to the specification as well
                document.specification['provider'] = document['provider']

    def _update_role_files_and_vars(self, action, document):
        """Render mandatory vars files for backup/recovery ansible roles inside the existing build directory."""

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
        """Update backup/recovery ansible playbooks inside the existing build directory and run the provisioning."""

        self.logger.info(f'Running {action} on {component}...')

        # Copy playbook file
        playbook_build_path = os.path.join(self.build_directory, 'ansible', f'{action}_{component}.yml')
        playbook_source_path = os.path.join(AnsibleRunner.ANSIBLE_PLAYBOOKS_PATH, f'{action}_{component}.yml')
        copy_file(playbook_source_path, playbook_build_path)

        # Run the playbook
        inventory_path = get_inventory_path_for_build(self.build_directory)
        self.ansible_command.run_playbook(inventory=inventory_path, playbook_path=playbook_build_path)
