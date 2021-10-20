import os
import stat

from cli.helpers.Step import Step
from cli.helpers.data_loader import BASE_DIR
from cli.helpers.Config import Config
from cli.helpers.build_io import copy_files_recursively


class PrepareEngine(Step):
    PREPARE_PATH = f'{BASE_DIR}/ansible/playbooks/roles/repository/files/download-requirements'
    COMMON_PATH = f'{PREPARE_PATH}/common'
    CHARTS_PATH = f'{BASE_DIR}/ansible/playbooks/roles/helm_charts/files/system'

    def __init__(self, input_data):
        super().__init__(__name__)
        self.os = input_data.os

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def prepare(self):
        prepare_src = os.path.join(self.PREPARE_PATH, self.os)

        prepare_dst = os.path.join(Config().output_dir, 'prepare_scripts')
        charts_dst = os.path.join(prepare_dst, 'charts', 'system')

        if not os.path.exists(prepare_src):
            supported_os = os.listdir(self.PREPARE_PATH)
            raise Exception(f'Unsupported OS: {self.os}. Currently supported: {supported_os}')

        # copy files to output dir
        copy_files_recursively(prepare_src, prepare_dst)
        copy_files_recursively(self.COMMON_PATH, os.path.join(prepare_dst, 'common'))
        copy_files_recursively(self.CHARTS_PATH, charts_dst)

        # make sure the scripts are executable
        self.make_file_executable(os.path.join(prepare_dst, 'download-requirements.sh'))

        self.logger.info(f'Prepared files for downloading the offline requirements in: {prepare_dst}')
        return 0

    @staticmethod
    def make_file_executable(file):
        executable_stat = os.stat(file)
        os.chmod(file, executable_stat.st_mode | stat.S_IEXEC)
