from src.command.command import Command
from src.error import DnfVariableNotfound


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

    def get_variable(self, name: str) -> str:
        process = self.run(['config-manager', '--dump-variables'])
        variables = [x for x in process.stdout.splitlines() if '=' in x]
        value = None

        for var in variables:
            chunks = var.split('=', maxsplit=1)
            if name == chunks[0].strip():
                value = chunks[1].strip()
                return value

        raise DnfVariableNotfound(f'Variable not found: {name}')
