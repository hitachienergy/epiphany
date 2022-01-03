import configparser


class FilterModule(object):
    """ Defines filters """

    def filters(self):
        return {
            'from_ini': self.from_ini,
            'get_ini_value': self.get_ini_value
        }

    def from_ini(self, content: str) -> str:
        """
        Parse `content` in ini format which was obtained from a decoded file.

        :param content: to be parsed
        :return: properly parsed ini content which can be further processed
        """
        return content.replace('\\n', '\n').replace('\\', '')

    def get_ini_value(self, content: str, field: str, section: str, accept_empty_field: bool = True) -> str:
        """
        Search for `field` in `content` under `section`
        Example:

        get_ini_value(content, 'some_field', 'some_section')

        Where content is:
        ```
        [some_section]
        some_filed = 150
        ```

        will return `150`

        :param content: where to search for section/field
        :param field: for which value will be searched for
        :param section: under which `field` should be search for
        :param accept_empty_field: if set to False will raise error on empty field or when section/field not found,
                                   empty string will be returned otherwise
        :return: value of `section/field`
        """
        config = configparser.ConfigParser()

        try:
            config.read_string(content)
        except configparser.MissingSectionHeaderError:
            # content might be missing default header, add it and try to parse it once more
            config = configparser.ConfigParser()
            config.read_string(f'[DEFAULT]\n{content}')

        if not accept_empty_field:
            return config[section][field]

        try:
            return config[section][field]
        except Exception:
            return ''
