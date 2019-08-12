from cli.helpers.Step import Step


class InfrastructureBuilder(Step):
    def __init__(self, docs):
        super().__init__(__name__)
        self.docs = docs

    def run(self):
        infrastructure = []

        return infrastructure

