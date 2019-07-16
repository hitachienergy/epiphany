import os

class Config:
    class __ConfigBase:
        def __init__(self):
            self._docker_cli = bool(os.environ.get('DOCKER_CLI', ''))

            self._output_dir = None
            if self._docker_cli:
                self._output_dir = '/shared/'

            self._log_file = 'log.log'
            self._log_format = '%(asctime)s %(levelname)s %(name)s - %(message)s'
            self._log_date_format = '%H:%M:%S'
            self._log_count = 10
            self._log_type = 'plain'

            self._validate_certs = True

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
                self._log_type = log_type

        @property
        def validate_certs(self):
            return self._validate_certs

        @validate_certs.setter
        def validate_certs(self, validate_certs):
            if not validate_certs is None:
                self._validate_certs = validate_certs

    instance = None

    def __new__(cls):
        if Config.instance is None:
            Config.instance = Config.__ConfigBase()
        return Config.instance
