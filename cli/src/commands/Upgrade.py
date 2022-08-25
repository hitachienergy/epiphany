import os
import re
import time
from pathlib import Path

from cli.src.Config import Config
from cli.src.Step import Step
from cli.src.ansible.AnsibleCommand import AnsibleCommand
from cli.src.ansible.AnsibleRunner import AnsibleRunner
from cli.src.helpers.build_io import copy_files_recursively
from cli.src.helpers.data_loader import load_schema_obj, schema_types
from cli.src.helpers.yaml_helpers import safe_load_all
from cli.src.schema.DefaultMerger import DefaultMerger
from cli.src.schema.ManifestHandler import ManifestHandler
from cli.src.schema.SchemaValidator import SchemaValidator


class Upgrade(Step):

    def __init__(self, input_data):
        super().__init__(__name__)
        self.__build_dir: Path = Path(input_data.build_directory)
        self.__manifest_file: Path = Path(self.__build_dir) / 'manifest.yml'
        self.ansible_options = {'forks': getattr(input_data, 'ansible_forks'),
                                'profile_tasks': getattr(input_data, 'profile_ansible_tasks', False)}
        self.file = getattr(input_data, 'file', "")
        self.backup_build_dir = ''
        self.ansible_command = AnsibleCommand()
        self.input_docs = []
        self.ping_retries: int = input_data.ping_retries

        Config().full_download = input_data.full_download
        Config().input_manifest_path = Path(self.file) if self.file else None

    def __filter_images(self, mhandler: ManifestHandler):
        selected_features = mhandler.get_selected_features()
        os_type = mhandler.cluster_model['specification']['cloud']['default_os_image']

        image_registry_doc = {}
        try:
            image_registry_doc = mhandler['configuration/image-registry'][0]
        except KeyError:
            image_registry_doc = load_schema_obj(schema_types.DEFAULT, 'common', 'configuration/image-registry')

        # filter out only image groups with matching features used by the cluster:
        os_arch = 'x86_64' if os_type == 'default' else os_type.split('-')[-1]
        image_groups = image_registry_doc['specification']['images_to_load'][os_arch]
        for image_group in image_groups:
            image_groups[image_group] = {feature: images for feature, images
                                         in image_groups[image_group].items()
                                         if feature in selected_features}

        mhandler.update_doc(image_registry_doc)

    def process_manifest(self):
        # This is only ran when the input file was not provided
        if self.file:
            return

        mhandler: ManifestHandler = ManifestHandler(build_path=self.__build_dir)
        mhandler.read_manifest()

        if not mhandler['configuration/feature-mappings']:
            return  # pre 2.0.1 manifest version

        self.__filter_images(mhandler)

        mhandler.write_manifest()

    def process_input_docs(self):
        # Check if we have input to load
        if not self.file:
            return

        # Load the user input YAML docs from the input file.
        self.input_mhandler: ManifestHandler = ManifestHandler(input_file=Path(self.file))
        if self.input_mhandler.exists():
            self.input_mhandler.read_manifest()

        # Some basic checking on the input document(s)
        if len(self.input_mhandler.docs) == 0:
            raise Exception('No documents in input file.')
        if not hasattr(self.input_mhandler.cluster_model, 'provider'):
            raise Exception('Input document does not have a provider.')

        # Merge the input docs with defaults
        with DefaultMerger(self.input_mhandler.docs) as doc_merger:
            self.input_docs = doc_merger.run()  # help

        # Validate input documents
        with SchemaValidator(self.input_mhandler.cluster_model.provider, self.input_mhandler.docs) as schema_validator:
            schema_validator.run()

    def get_backup_dirs(self):
        result = []
        for d in os.listdir(self.__build_dir):
            bd = os.path.join(self.__build_dir, d)
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
        self.backup_build_dir = os.path.join(self.__build_dir, backup_dir_name )
        self.logger.info(f'Backing up build dir to "{self.backup_build_dir}"')
        copy_files_recursively(self.__build_dir, self.backup_build_dir)

    def upgrade(self):
        # backup existing build
        self.backup_build()

        # Load possible input docs
        self.process_input_docs()

        # Load existing manifest and process it
        self.process_manifest()

        # Run Ansible to upgrade infrastructure
        with AnsibleRunner(build_dir=self.__build_dir, backup_build_dir=self.backup_build_dir,
                           ansible_options=self.ansible_options, config_docs=self.input_docs,
                           ping_retries=self.ping_retries) as ansible_runner:
            ansible_runner.upgrade()

        return 0
