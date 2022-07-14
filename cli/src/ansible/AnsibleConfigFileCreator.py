import os
from collections import OrderedDict

from cli.src.Config import Config
from cli.src.helpers.build_io import save_ansible_config_file
from cli.src.Step import Step


class AnsibleConfigFileCreator(Step):
    def __init__(self, ansible_options, ansible_config_file_path):
        super().__init__(__name__)
        self.ansible_options = ansible_options
        self.ansible_config_file_path = ansible_config_file_path
        self.ansible_config_file_settings = OrderedDict()

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def get_setting(self, section, key):
        setting = None
        if section in self.ansible_config_file_settings:
            setting = self.ansible_config_file_settings[section].get(key)
        return setting

    def add_setting(self, section, key, value):
        if section not in self.ansible_config_file_settings:
            self.ansible_config_file_settings[section] = {}
        if key not in self.ansible_config_file_settings[section]:
            self.ansible_config_file_settings[section].update({key: value})
        else:
            raise TypeError(f"Setting {section}[{key}] already exists")

    def update_setting(self, section, key, value, append=False):
        if (section not in self.ansible_config_file_settings or
            key not in self.ansible_config_file_settings[section]):
            self.add_setting(section, key, value)
        else:
            if type(self.ansible_config_file_settings[section][key]) is list and append:
                self.ansible_config_file_settings[section][key].append(value)
            else:
                self.ansible_config_file_settings[section][key] = value

    def process_ansible_options(self):
        self.add_setting('defaults', 'allow_world_readable_tmpfiles', 'true')  # workaround for delegate_to with become_user
        if self.ansible_options['profile_tasks']:
            self.add_setting('defaults', 'callback_whitelist', ['profile_tasks'])
        self.add_setting('defaults', 'forks', self.ansible_options['forks'])
        # Ubuntu 18 upgraded to 20 has Python 2 and 3 so 'auto_legacy' doesn't work for PostgreSQL Ansible modules
        self.add_setting('defaults', 'interpreter_python', 'auto')
        if not Config().no_color:
            self.add_setting('defaults', 'force_color', 'true')

    def create(self):
        self.logger.info('Creating ansible.cfg')
        self.process_ansible_options()
        save_ansible_config_file(self.ansible_config_file_settings, self.ansible_config_file_path)
        os.environ["ANSIBLE_CONFIG"] = self.ansible_config_file_path
