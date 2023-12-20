import shutil

from cli.src.Log import Log
from cli.src.Step import Step

from cli.src.helpers.data_loader import load_yamls_file
from cli.src.helpers.yaml_helpers import dump_all


class FormatManifest(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.logger = Log(__name__)
        self.input_manifest = input_data.input_manifest
        self.with_backup = input_data.with_backup


    def format(self):
        """
        Load input manifest and save it.
        """

        docs = load_yamls_file(self.input_manifest)

        # Make backup
        if self.with_backup:
            backup_path = self.input_manifest + '.bak'
            self.logger.info(f'Creating backup: {backup_path}')
            shutil.copy2(self.input_manifest, backup_path)

        # Overwrite manifest
        with open(file=self.input_manifest, mode='w', encoding='utf-8') as stream:
            dump_all(docs, stream)

        return 0
