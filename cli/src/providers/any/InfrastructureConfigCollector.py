from cli.src.helpers.Step import Step
from cli.src.helpers.doc_list_helpers import select_single


class InfrastructureConfigCollector(Step):

    def __init__(self, docs):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.docs = docs

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        pass
