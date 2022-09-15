from cli.src.helpers.doc_list_helpers import select_single
from cli.src.Step import Step


class InfrastructureConfigCollector(Step):

    def __init__(self, docs):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.docs = docs

    def run(self):
        pass
