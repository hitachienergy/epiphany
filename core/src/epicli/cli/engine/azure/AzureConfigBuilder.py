from engine.Step import Step


class AzureConfigBuilder(Step):
    def __init__(self):
        super().__init__(__name__)

    def run(self):
        raise NotImplementedError()

