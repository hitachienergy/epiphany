from cli.helpers.doc_list_helpers import select_first
from cli.helpers.Log import Log
from cli.models.AnsibleHostModel import AnsibleHostModel


class APIProxy:
    def __init__(self, cluster_model, config_docs):
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.logger = Log(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def get_ips_for_feature(self, component_key):
        component_config = self.cluster_model.specification.components[component_key]
        result = []
        if hasattr(component_config, 'machines'):
            for machine in component_config.machines:
                machine_doc = select_first(self.config_docs,
                                           lambda x: x.kind == 'infrastructure/machine' and x.name == machine)
                result.append(AnsibleHostModel(machine_doc.specification.hostname, machine_doc.specification.ip))
        return result
