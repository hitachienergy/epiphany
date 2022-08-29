import copy
import os
from pathlib import Path

from cli.src.ansible.AnsibleCommand import AnsibleCommand
from cli.src.helpers.build_io import (copy_file, copy_files_recursively,
                                      get_ansible_config_file_path_for_build,
                                      get_inventory_path_for_build)
from cli.src.helpers.data_loader import (ANSIBLE_PLAYBOOK_PATH,
                                         load_schema_obj, schema_types)
from cli.src.helpers.doc_list_helpers import (ExpectedSingleResultException,
                                              select_single)
from cli.src.helpers.yaml_helpers import dump
from cli.src.schema.DefaultMerger import DefaultMerger
from cli.src.schema.ManifestHandler import ManifestHandler
from cli.src.schema.SchemaValidator import SchemaValidator
from cli.src.Step import Step
from cli.version import VERSION


class BackupRecoveryBase(Step):
    """Perform backup and recovery operations (abstract base class)."""

    def __init__(self, input_data):
        # super(BackupRecoveryBase, self).__init__(__name__) needs to be called in any subclass
        self.input_manifest: Path = Path(input_data.input_manifest)
        self.build_directory = input_data.build_directory
        self.mhandler: ManifestHandler = ManifestHandler(build_path=Path(self.build_directory))
        self.input_docs = []
        self.configuration_docs = []
        self.cluster_model = None
        self.backup_doc = None
        self.recovery_doc = None
        self.ansible_command = AnsibleCommand()
        self.ansible_config_file_path = get_ansible_config_file_path_for_build(input_data.build_directory)

    def _process_input_docs(self):
        """Load, validate and merge (with defaults) input yaml documents."""

        # Get existing manifest config documents
        self.mhandler.read_manifest()
        self.cluster_model = self.mhandler.cluster_model

        # Load only backup / recovery configuration documents
        backup_mhandler: ManifestHandler = ManifestHandler(input_file=self.input_manifest)
        backup_mhandler.read_manifest()
        self.input_docs = backup_mhandler['configuration/backup'] + backup_mhandler['configuration/recovery']
        if len(self.input_docs) < 1:
            raise Exception('No documents for backup or recovery in input file.')

        # Validate input documents
        with SchemaValidator(self.cluster_model.provider, self.input_docs) as schema_validator:
            schema_validator.run_for_individual_documents()

        # Merge the input docs with defaults
        with DefaultMerger(self.input_docs) as doc_merger:
            self.input_docs = doc_merger.run()

    def _process_configuration_docs(self):
        """Populate input yaml documents with additional required ad-hoc data."""

        # Seed the self.configuration_docs
        self.configuration_docs = copy.deepcopy(self.input_docs)

        # Please notice using DefaultMerger is not needed here, since it is done already at this point.
        # We just check if documents are missing and insert default ones without the unneeded merge operation.
        for kind in ('configuration/backup', 'configuration/recovery'):
            try:
                # Check if the required document is in user inputs
                document = select_single(self.configuration_docs, lambda x: x.kind == kind)
            except ExpectedSingleResultException:
                # If there is no document provided by the user, then fallback to defaults
                document = load_schema_obj(schema_types.DEFAULT, 'common', kind)
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
        roles_source_path = os.path.join(ANSIBLE_PLAYBOOK_PATH, 'roles', action)
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
        playbook_source_path = os.path.join(ANSIBLE_PLAYBOOK_PATH, f'{action}_{component}.yml')
        copy_file(playbook_source_path, playbook_build_path)

        # Run the playbook
        inventory_path = get_inventory_path_for_build(self.build_directory)
        self.ansible_command.run_playbook(inventory=inventory_path, playbook_path=playbook_build_path)
