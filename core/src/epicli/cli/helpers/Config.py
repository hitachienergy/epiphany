import os

class Config:
    class __ConfigBase:
        def __init__(self):
            self._docker_cli = os.environ.get('DOCKER_CLI', False)
            self._log_file = 'log.json'
            self._output_dir = os.path.join(os.path.dirname(__file__), '../../output/')
            if self._docker_cli:
                self._output_dir = '/shared/'

        @property
        def output_dir(self):
            return self._output_dir

        @output_dir.setter
        def output_dir(self, output_dir):
            if self._docker_cli or output_dir is None:
                return
            self._output_dir = output_dir

        @property
        def log_file(self):
            return self._log_file

        @log_file.setter
        def log_file(self, log_file):
            if log_file is None:
                return
            self._log_file = log_file

        @property
        def docker_cli(self):
            return self._docker_cli

    instance = None

    def __new__(cls):
        if Config.instance is None:
            Config.instance = Config.__ConfigBase()
        return Config.instance
