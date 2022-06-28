from pathlib import Path

from src.command.command import Command


class AptKey(Command):
    """
    Interface for `apt-key` tool.
    """

    def __init__(self, retries: int):
        super().__init__('apt-key', retries)

    def add(self, key: Path):
        """
        Interface for `apt-key add`

        :key: key as file to be added
        """
        self.run(['add', str(key)])
