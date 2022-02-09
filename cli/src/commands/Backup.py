import os
from cli.src.helpers.doc_list_helpers import select_single
from cli.src.commands.BackupRecoveryBase import BackupRecoveryBase


class Backup(BackupRecoveryBase):
    """Perform backup operations."""

    def __init__(self, input_data):
        super(BackupRecoveryBase, self).__init__(__name__)  # late call of the Step.__init__(__name__)
        super(Backup, self).__init__(input_data)

    def backup(self):
        """Backup all enabled components."""

        self._process_input_docs()
        self._process_configuration_docs()

        # Get backup config document
        backup_doc = select_single(self.configuration_docs, lambda x: x.kind == 'configuration/backup')

        self._update_role_files_and_vars('backup', backup_doc)

        # Set env
        self.logger.info(f'ANSIBLE_CONFIG={self.ansible_config_file_path}')
        os.environ["ANSIBLE_CONFIG"] = self.ansible_config_file_path

        # Execute all enabled component playbooks sequentially
        for component_name, component_config in sorted(backup_doc.specification.components.items()):
            if component_config.enabled:
                self._update_playbook_files_and_run('backup', component_name)

        return 0
