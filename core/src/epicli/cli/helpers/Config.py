import os

class Config:
    class __ConfigBase:
        def __init__(self):
            self._docker_cli = bool(os.environ.get('DOCKER_CLI', ''))

            self._output_dir = os.path.join(os.path.dirname(__file__), '../../output/')
            if self._docker_cli:
                self._output_dir = '/shared/'

            self._log_file = 'log.json'
            self._log_format = '%(asctime)s %(levelname)s %(name)s - %(message)s'
            self._log_date_format = '%H:%M:%S'
            self._log_count = 10

        @property
        def docker_cli(self):
            return self._docker_cli

        @property
        def output_dir(self):
            return self._output_dir

        @output_dir.setter
        def output_dir(self, output_dir):
            if not self._docker_cli and not output_dir is None:
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



    instance = None

    def __new__(cls):
        if Config.instance is None:
            Config.instance = Config.__ConfigBase()
        return Config.instance
