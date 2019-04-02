from engine.Step import Step


class AzureConfigBuilder(Step):
    def __init__(self):
        Step.__init__(self, __name__)

    def run(self):
        raise NotImplementedError()

