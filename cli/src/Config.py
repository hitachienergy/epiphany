import os
from os.path import expanduser
from pathlib import Path
from typing import Dict, List


LOG_TYPES = ['plain', 'json']


SUPPORTED_OS: Dict[str, List[str]] = {
    'almalinux-8': ['x86_64','aarch64'],
    'rhel-8': ['x86_64'],
    'ubuntu-20.04': ['x86_64']
}


class InvalidLogTypeException(Exception):
    pass


class Config:
    class __ConfigBase:
        def __init__(self):
            self._docker_cli = bool(os.environ.get('EPICLI_DOCKER_SHARED_DIR',''))

            self._output_dir = None
            if self._docker_cli:
                self._output_dir = os.path.join(os.environ.get('EPICLI_DOCKER_SHARED_DIR'), 'build')

            self._log_file = 'log.log'
            self._log_format = '%(asctime)s %(levelname)s %(name)s - %(message)s'
            self._log_date_format = '%H:%M:%S'
            self._log_count = 10
            self._log_type = 'plain'

            self._full_download: bool = False
            self._input_manifest_path: Path = None
            self._validate_certs = True
            self._debug = 0
            self._auto_approve = False
            self._offline_requirements = ''
            self._wait_for_pods = False
            self._upgrade_components = []
            self._vault_password_location = os.path.join(expanduser("~"), '.epicli/vault.cfg')
            self._no_color: bool = False

        @property
        def full_download(self) -> bool:
            return self._full_download

        @full_download.setter
        def full_download(self, full_download: bool):
            self._full_download = full_download

        @property
        def input_manifest_path(self) -> Path:
            return self._input_manifest_path

        @input_manifest_path.setter
        def input_manifest_path(self, input_manifest_path: Path):
            self._input_manifest_path = input_manifest_path

        @property
        def docker_cli(self):
            return self._docker_cli

        @property
        def output_dir(self):
            return self._output_dir

        @output_dir.setter
        def output_dir(self, output_dir):
            if not self._docker_cli and output_dir is not None:
                self._output_dir = output_dir

        @property
        def log_file(self):
            return self._log_file

        @log_file.setter
        def log_file(self, log_file):
            if log_file is not None:
                self._log_file = log_file

        @property
        def log_format(self):
            return self._log_format

        @log_format.setter
        def log_format(self, log_format):
            if log_format is not None:
                self._log_format = log_format

        @property
        def log_date_format(self):
            return self._log_date_format

        @log_date_format.setter
        def log_date_format(self, log_date_format):
            if log_date_format is not None:
                self._log_date_format = log_date_format

        @property
        def log_count(self):
            return self._log_count

        @log_count.setter
        def log_count(self, log_count):
            if log_count is not None:
                self._log_count = log_count

        @property
        def log_type(self):
            return self._log_type

        @log_type.setter
        def log_type(self, log_type):
            if log_type is not None:
                if log_type in LOG_TYPES:
                    self._log_type = log_type
                else:
                    raise InvalidLogTypeException( f'log_type "{log_type}" is not valid. Use one of: {LOG_TYPES}' )

        @property
        def validate_certs(self):
            return self._validate_certs

        @validate_certs.setter
        def validate_certs(self, validate_certs):
            if validate_certs is not None:
                self._validate_certs = validate_certs

        @property
        def debug(self):
            return self._debug

        @debug.setter
        def debug(self, debug):
            if debug is not None:
                self._debug = debug

        @property
        def auto_approve(self):
            return self._auto_approve

        @auto_approve.setter
        def auto_approve(self, auto_approve):
            if auto_approve is not None:
                self._auto_approve = auto_approve

        @property
        def vault_password_location(self):
            return self._vault_password_location

        @vault_password_location.setter
        def vault_password_location(self, vault_password_location):
            if vault_password_location is not None:
                self._vault_password_location = vault_password_location

        @property
        def offline_requirements(self):
            return self._offline_requirements

        @offline_requirements.setter
        def offline_requirements(self, offline_requirements):
            if offline_requirements is not None:
                if not os.path.isdir(offline_requirements):
                    raise Exception(f'offline_requirements path "{offline_requirements}" is not a valid path.')

                # To make sure Ansible copies the content of the folder the the repository host.
                if not offline_requirements.endswith('/'):
                    offline_requirements =  f'{offline_requirements}/'
                self._offline_requirements = offline_requirements

        @property
        def wait_for_pods(self):
            return self._wait_for_pods

        @wait_for_pods.setter
        def wait_for_pods(self, wait_for_pods):
            if wait_for_pods is not None:
                self._wait_for_pods = wait_for_pods

        @property
        def upgrade_components(self):
            return self._upgrade_components

        @upgrade_components.setter
        def upgrade_components(self, upgrade_components):
            self._upgrade_components = upgrade_components

        @property
        def no_color(self) -> bool:
            return self._no_color

        @no_color.setter
        def no_color(self, no_color: bool):
            self._no_color = no_color

    instance = None

    def __new__(cls):
        if Config.instance is None:
            Config.instance = Config.__ConfigBase()
        return Config.instance
