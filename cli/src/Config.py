import os
from os.path import expanduser
from typing import Dict, List


LOG_TYPES = ['plain', 'json']


SUPPORTED_OS: Dict[str, List[str]] = {
    'almalinux-8': ['x86_64'],
    'almalinux-8': ['aarch64'],
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

            self._validate_certs = True
            self._debug = 0
            self._auto_approve = False
            self._offline_requirements = ''
            self._wait_for_pods = False
            self._upgrade_components = []
            self._vault_password_location = os.path.join(expanduser("~"), '.epicli/vault.cfg')

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
            if not log_file is None:
                self._log_file = log_file

        @property
        def log_format(self):
            return self._log_format

        @log_format.setter
        def log_format(self, log_format):
            if not log_format is None:
                self._log_format = log_format

        @property
        def log_date_format(self):
            return self._log_date_format

        @log_date_format.setter
        def log_date_format(self, log_date_format):
            if not log_date_format is None:
                self._log_date_format = log_date_format

        @property
        def log_count(self):
            return self._log_count

        @log_count.setter
        def log_count(self, log_count):
            if not log_count is None:
                self._log_count = log_count

        @property
        def log_type(self):
            return self._log_type

        @log_type.setter
        def log_type(self, log_type):
            if not log_type is None:
                if log_type in LOG_TYPES:
                    self._log_type = log_type
                else:
                    raise InvalidLogTypeException( f'log_type "{log_type}" is not valid. Use one of: {LOG_TYPES}' )

        @property
        def validate_certs(self):
            return self._validate_certs

        @validate_certs.setter
        def validate_certs(self, validate_certs):
            if not validate_certs is None:
                self._validate_certs = validate_certs

        @property
        def debug(self):
            return self._debug

        @debug.setter
        def debug(self, debug):
            if not debug is None:
                self._debug = debug

        @property
        def auto_approve(self):
            return self._auto_approve

        @auto_approve.setter
        def auto_approve(self, auto_approve):
            if not auto_approve is None:
                self._auto_approve = auto_approve

        @property
        def vault_password_location(self):
            return self._vault_password_location

        @vault_password_location.setter
        def vault_password_location(self, vault_password_location):
            if not vault_password_location is None:
                self._vault_password_location = vault_password_location

        @property
        def offline_requirements(self):
            return self._offline_requirements

        @offline_requirements.setter
        def offline_requirements(self, offline_requirements):
            if not offline_requirements is None:
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
            if not wait_for_pods is None:
                self._wait_for_pods = wait_for_pods

        @property
        def upgrade_components(self):
            return self._upgrade_components

        @upgrade_components.setter
        def upgrade_components(self, upgrade_components):
            self._upgrade_components = upgrade_components

    instance = None

    def __new__(cls):
        if Config.instance is None:
            Config.instance = Config.__ConfigBase()
        return Config.instance
