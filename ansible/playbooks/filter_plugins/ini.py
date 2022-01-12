from typing import Dict
import configparser


class FilterModule(object):
    """ Defines filters """

    def filters(self):
        return {
            'from_ini': self.from_ini,
        }

    def from_ini(self, content: str, default_section_name: str = '__none__') -> Dict:
        """
        Parse `content` in ini format which was obtained from a decoded file.

        :param content: to be parsed
        :param default_section_name: fields without section will be available under this key
        :return: properly parsed ini content
        """
        fixed_content = content.replace('\\n', '\n').replace('\\', '')

        config = configparser.ConfigParser()

        try:
            config.read_string(fixed_content)
        except configparser.MissingSectionHeaderError:
            # content might be missing default header, add it and try to parse it once more
            config = configparser.ConfigParser()
            config.read_string(f'[{default_section_name}]\n{fixed_content}')

        return {section: dict(config.items(section)) for section in config.sections()}
