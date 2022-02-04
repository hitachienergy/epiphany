import os
import stat
from pathlib import Path
from shutil import copy, copytree
from typing import Dict

from cli.src.Config import Config
from cli.src.helpers.data_loader import BASE_DIR
from cli.src.Step import Step


class Prepare(Step):
    PREPARE_PATH: Path = Path(f'{BASE_DIR}/ansible/playbooks/roles/repository/files/download-requirements')
    CHARTS_PATH: Path = Path(f'{BASE_DIR}/ansible/playbooks/roles/helm_charts/files/system')

    def __init__(self, input_data):
        super().__init__(__name__)
        self.os: str = input_data.os
        self.arch: str = input_data.arch
        self.output_dir: str = input_data.output_dir

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def prepare(self) -> int:
        repositories_path: Path = self.PREPARE_PATH / 'repositories'
        repositories_arch_path: Path = repositories_path / f'{self.arch}'

        if not repositories_arch_path.exists():
            raise Exception(f'Unsupported Arch type: {self.arch}. Currently supported: x86_64|arm64')

        repositories_file_path: Path = repositories_arch_path / f'{self.os}.yml'

        requirements_path: Path = self.PREPARE_PATH / 'requirements'
        arch_path: Path = requirements_path / self.arch

        if not arch_path.exists():
            raise Exception(f'Unsupported Arch type: {self.arch}. Currently supported: x86_64|arm64')

        distro_path: Path = arch_path / self.os

        if not arch_path.exists():
            raise Exception(f'Unsupported OS: {self.os} for chosen arch: {self.arch}. '
                            'Currently supported OS: redhat-7|ubuntu-20.04')

        dest_path: Path = Path(Config().output_dir)
        dest_path /= self.output_dir if self.output_dir else 'prepare_scripts'
        charts_path = dest_path / 'charts/system'

        # source : destination
        download_requirements_paths: Dict[Path, Path] = {
            arch_path / 'cranes.yml':                       dest_path / f'requirements/{self.arch}',
            arch_path / 'files.yml':                        dest_path / f'requirements/{self.arch}',
            arch_path / 'images.yml':                       dest_path / f'requirements/{self.arch}',
            charts_path:                                    dest_path / 'charts/system',
            distro_path / 'packages.yml':                   dest_path / f'requirements/{self.arch}/{self.os}',
            repositories_file_path:                         dest_path / 'repositories',
            requirements_path / 'grafana-dashboards.yml':   dest_path / 'requirements',
            self.PREPARE_PATH / 'download-requirements.py': dest_path,
            self.PREPARE_PATH / 'poyo':                     dest_path / 'poyo',
            self.PREPARE_PATH / 'src':                      dest_path / 'src',
        }

        distro_files: Path = distro_path / 'files.yml'
        if distro_files.exists():  # specific files for target distro are optional
            download_requirements_paths[distro_files] = dest_path / f'requirements/{self.arch}/{self.os}'

        # copy files to output dir
        for source, destination in download_requirements_paths.items():
            destination.mkdir(exist_ok=True, parents=True)
            if source.is_dir():
                copytree(source, destination, dirs_exist_ok=True)
            else:
                copy(source, destination)

        # make sure the scripts are executable
        self.make_file_executable(dest_path / 'download-requirements.py')

        self.logger.info(f'Prepared files for downloading the offline requirements in: {dest_path}')
        return 0

    @staticmethod
    def make_file_executable(file: Path):
        executable_stat = os.stat(file)
        os.chmod(file, executable_stat.st_mode | stat.S_IEXEC)
