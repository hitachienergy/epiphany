from src.command.command import Command


class YumConfigManager(Command):
    """
    Interface for `yum-config-manager`
    """

    def __init__(self, retries: int):
        super().__init__('yum-config-manager', retries)

    def enable_repo(self, repo: str):
        self.run(['--enable', repo])

    def add_repo(self, repo: str):
        self.run(['--add-repo', repo])

    def disable_repo(self, repo: str):
        self.run(['--disable', repo])
