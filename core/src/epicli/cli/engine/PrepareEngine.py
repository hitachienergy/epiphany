import os
import stat
import inspect
import shutil
from  os.path import dirname

from cli.helpers.Step import Step
from cli.helpers.data_loader import DATA_FOLDER_PATH
from cli.helpers.Config import Config
from cli.helpers.build_saver import copy_files_recursively


class PrepareEngine(Step):
    PREPARE_PATH = DATA_FOLDER_PATH + '/common/ansible/playbooks/roles/repository/files/download-requirements'
    CHARTS_PATH = DATA_FOLDER_PATH + '/common/ansible/playbooks/roles/helm_charts/files/system'

    def __init__(self, input_data):
        super().__init__(__name__)
        self.os = input_data.os

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def prepare(self):
        prepare_src = os.path.join(self.PREPARE_PATH, self.os)
        charts_src = self.CHARTS_PATH
        skopeo_src = os.path.join(dirname(dirname(inspect.getfile(os))), 'skopeo_linux')

        prepare_dst = os.path.join(Config().output_dir, 'prepare_scripts')
        charts_dst = os.path.join(prepare_dst, 'charts', 'system')

        if not os.path.exists(prepare_src):
            supported_os = os.listdir(self.PREPARE_PATH)
            raise Exception(f'Unsupported OS: {self.os}. Currently supported: {supported_os}')

        if not os.path.exists(skopeo_src):
            raise Exception('Skopeo dependency not found')

        # copy files to output dir
        copy_files_recursively(prepare_src, prepare_dst)
        copy_files_recursively(charts_src, charts_dst)
        shutil.copy(skopeo_src, prepare_dst)

        # make sure the scripts and skopeo are executable
        self.make_file_executable(os.path.join(prepare_dst, 'skopeo_linux'))
        self.make_file_executable(os.path.join(prepare_dst, 'download-requirements.sh'))

        self.logger.info(f'Prepared files for downloading the offline requirements in: {prepare_dst}')
        return 0

    @staticmethod
    def make_file_executable(file):
        executable_stat = os.stat(file)
        os.chmod(file, executable_stat.st_mode | stat.S_IEXEC)
