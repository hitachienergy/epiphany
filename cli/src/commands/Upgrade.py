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
from cli.src.schema.DefaultMerger import DefaultMerger
from cli.src.schema.ManifestHandler import ManifestHandler
from cli.src.schema.SchemaValidator import SchemaValidator


class Upgrade(Step):

    def __init__(self, input_data):
        super().__init__(__name__)
        self.__build_dir: Path = Path(input_data.build_directory)
        self.ansible_options = {'forks': getattr(input_data, 'ansible_forks'),
                                'profile_tasks': getattr(input_data, 'profile_ansible_tasks', False)}
        self.input_manifest_path = getattr(input_data, 'input_manifest', None)
        self.backup_build_dir = ''
        self.ansible_command = AnsibleCommand()
        self.input_docs = []
        self.ping_retries: int = input_data.ping_retries

        Config().full_download = input_data.full_download
        Config().input_manifest_path = Path(self.input_manifest_path) if self.input_manifest_path else None

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

    def process_input_docs(self) -> ManifestHandler:
        # Check if we have input to load
        if not self.input_manifest_path:
            return ManifestHandler(build_path=self.__build_dir)

        # Load the user input YAML docs from the input file.
        input_mhandler: ManifestHandler = ManifestHandler(input_file=Path(self.input_manifest_path))
        if input_mhandler.exists():
            input_mhandler.read_manifest()

        # Some basic checking on the input document(s)
        if len(input_mhandler.docs) == 0:
            raise Exception('No documents in input file.')
        if not hasattr(input_mhandler.docs[0], 'provider'):
            raise Exception('Input document does not have a provider.')

        # Merge the input docs with defaults
        with DefaultMerger(input_mhandler.docs) as doc_merger:
            input_mhandler.update_docs(doc_merger.run())

        # Validate input documents
        with SchemaValidator(input_mhandler.docs[0].provider, input_mhandler.docs) as schema_validator:
            schema_validator.run()

        if input_mhandler['epiphany-cluster'] and input_mhandler['configuration/feature-mappings']:
            self.__filter_images(input_mhandler)

        return input_mhandler

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
        mhandler = self.process_input_docs()

        # Run Ansible to upgrade infrastructure
        with AnsibleRunner(build_dir=self.__build_dir, backup_build_dir=self.backup_build_dir,
                           ansible_options=self.ansible_options, config_docs=mhandler.docs,
                           ping_retries=self.ping_retries) as ansible_runner:
            ansible_runner.upgrade()

        return 0
