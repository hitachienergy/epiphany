from cli.helpers.doc_list_helpers import select_single
from cli.engine.BackupRecoveryEngineBase import BackupRecoveryEngineBase


class RecoveryEngine(BackupRecoveryEngineBase):
    """Perform recovery operations."""

    def __init__(self, input_data):
        super(BackupRecoveryEngineBase, self).__init__(__name__)  # late call of the Step.__init__(__name__)
        super(RecoveryEngine, self).__init__(input_data)

    def recovery(self):
        """Recover all enabled components."""

        self._process_input_docs()
        self._process_configuration_docs()

        # Get recovery config document
        recovery_doc = select_single(self.configuration_docs, lambda x: x.kind == 'configuration/recovery')

        self._update_role_files_and_vars('recovery', recovery_doc)

        # Execute all enabled component playbooks sequentially
        for component_name, component_config in sorted(recovery_doc.specification.components.items()):
            if component_config.enabled:
                self._update_playbook_files_and_run('recovery', component_name)

        return 0
