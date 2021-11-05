from src.command.command import Command


class Apt(Command):
    """
    Interface for `apt` tool.
    """

    def __init__(self, retries: int):
        super().__init__('apt', retries)

    def update(self):
        """
        Interface for `apt-get update`
        """
        self.run(['update'])


    def download(self, package: str):
        """
        Interface for `apt download package`

        :param package: package to be downloaded
        """
        self.run(['download', package])

    def install(self, package: str, assume_yes: bool = True):
        """
        Interface for `apt install package`

        :param package: package to be installed
        :param assume_yes: if set to True `-y` flag will be added
        """
        no_ask: str = '-y' if assume_yes else ''
        self.run(['install', no_ask, package])
