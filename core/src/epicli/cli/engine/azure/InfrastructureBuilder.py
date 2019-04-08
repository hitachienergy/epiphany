from cli.helpers.Step import Step


class ConfigBuilder(Step):
    def __init__(self):
        super().__init__(__name__)

    def run(self):
        raise NotImplementedError()

