from cli.helpers.Step import Step


class TemplateGenerator(Step):

    def __init__(self, cluster_model, infrastructure):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.infrastructure = [cluster_model] + infrastructure

    def run(self):
        pass