import os
import time
import re

from cli.helpers.Step import Step
from cli.engine.ansible.AnsibleCommand import AnsibleCommand
from cli.engine.ansible.AnsibleRunner import AnsibleRunner
from cli.helpers.yaml_helpers import safe_load_all
from cli.engine.schema.DefaultMerger import DefaultMerger
from cli.engine.schema.SchemaValidator import SchemaValidator
from cli.helpers.build_io import copy_files_recursively


class UpgradeEngine(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.build_dir = input_data.build_directory
        self.ansible_options = {'profile_tasks': getattr(input_data, 'profile_ansible_tasks', False)}
        self.file = getattr(input_data, 'file', "")
        self.backup_build_dir = ''
        self.ansible_command = AnsibleCommand()
        self.input_docs = []
        self.__ping_retries: int = input_data.ping_retries

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def process_input_docs(self):
        # Check if we have input to load
        if not self.file:
            return

        # Load the user input YAML docs from the input file.
        if os.path.isabs(self.file):
            path_to_load = self.file
        else:
            path_to_load = os.path.join(os.getcwd(), self.file)
        user_file_stream = open(path_to_load, 'r')
        self.input_docs = safe_load_all(user_file_stream)

        # Some basic checking on the input document(s)
        if len(self.input_docs) == 0:
            raise Exception('No documents in input file.')
        if not hasattr(self.input_docs[0], 'provider'):
            raise Exception('Input document does not have a provider.')

        # Merge the input docs with defaults
        with DefaultMerger(self.input_docs) as doc_merger:
            self.input_docs = doc_merger.run()

        # Validate input documents
        with SchemaValidator(self.input_docs[0].provider, self.input_docs) as schema_validator:
            schema_validator.run()

    def get_backup_dirs(self):
        result = []
        for d in os.listdir(self.build_dir):
            bd = os.path.join(self.build_dir, d)
            if os.path.isdir(bd) and re.match(r'backup_\d', d): result.append(bd)
        return result

    def backup_build(self):
        # check if there are backup dirs and if so take the latest to work with.
        backup_dirs = self.get_backup_dirs()
        if len(backup_dirs) > 0:
            self.backup_build_dir = max(backup_dirs , key=os.path.getmtime)
            self.logger.info(f'There is already a backup present. Using latest for upgrade: "{self.backup_build_dir}"')
            return

        # no backup dir so use the latest
        backup_dir_name = f'backup_{int(round(time.time() * 1000))}'
        self.backup_build_dir = os.path.join(self.build_dir, backup_dir_name )
        self.logger.info(f'Backing up build dir to "{self.backup_build_dir}"')
        copy_files_recursively(self.build_dir, self.backup_build_dir)

    def upgrade(self):
        # backup existing build
        self.backup_build()

        # Load possible input docs
        self.process_input_docs()

        # Run Ansible to upgrade infrastructure
        with AnsibleRunner(build_dir=self.build_dir, backup_build_dir=self.backup_build_dir,
                           ansible_options=self.ansible_options, config_docs=self.input_docs,
                           ping_retries=self.__ping_retries) as ansible_runner:
            ansible_runner.upgrade()

        return 0
