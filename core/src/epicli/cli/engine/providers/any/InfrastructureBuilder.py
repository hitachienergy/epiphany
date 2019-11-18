from cli.helpers.Step import Step
from cli.helpers.doc_list_helpers import select_single, select_all
from cli.version import VERSION

class InfrastructureBuilder(Step):
    def __init__(self, docs):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.docs = docs

    def run(self):
        infrastructure_docs = select_all(self.docs, lambda x: x.kind.startswith('infrastructure/'))

        for i in range(len(infrastructure_docs)): 
            infrastructure_docs[i]['version'] = VERSION          
    
        return infrastructure_docs
