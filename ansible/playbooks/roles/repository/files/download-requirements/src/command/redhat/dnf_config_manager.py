from src.command.command import Command


class DnfConfigManager(Command):
    """
    Interface for `dnf config-manager`
    """

    def __init__(self, retries: int):
        super().__init__('dnf', retries)

    def add_repo(self, repo: str):
        self.run(['config-manager', '--add-repo', repo])

    def disable_repo(self, repo: str):
        self.run(['config-manager', '--set-disabled', repo])

    def enable_repo(self, repo: str):
        self.run(['config-manager', '--set-enabled', repo])
