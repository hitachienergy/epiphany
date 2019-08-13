from cli.helpers.Step import Step
from cli.helpers.naming_helpers import resource_name
from cli.helpers.doc_list_helpers import select_single, select_all
from cli.helpers.doc_list_helpers import select_first
from cli.helpers.data_loader import load_yaml_obj, types

class InfrastructureBuilder(Step):
    def __init__(self, docs):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.cluster_name = self.cluster_model.specification.name.lower()
        self.cluster_prefix = self.cluster_model.specification.prefix.lower()
        self.resource_group_name = resource_name(self.cluster_prefix, self.cluster_name, 'rg')
        self.region = self.cluster_model.specification.cloud.region
        self.docs = docs

    def run(self):
        infrastructure = []

        resource_group = self.get_resource_group()
        infrastructure.append(resource_group)        

        vnet = self.get_virtual_network()
        infrastructure.append(vnet)

        return infrastructure

    def get_resource_group(self):
        resource_group = self.get_config_or_default(self.docs, 'infrastructure/resource-group')
        resource_group.specification.name = self.resource_group_name
        resource_group.specification.region = self.cluster_model.specification.cloud.region
        return resource_group    

    def get_virtual_network(self):
        vnet = self.get_config_or_default(self.docs, 'infrastructure/vnet')
        vnet.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'vnet')
        vnet.specification.address_space = self.cluster_model.specification.cloud.vnet_address_pool
        vnet.specification.resource_group_name = self.resource_group_name
        vnet.specification.location = self.cluster_model.specification.cloud.region
        return vnet            
    
    @staticmethod
    def get_config_or_default(docs, kind):
        config = select_first(docs, lambda x: x.kind == kind)
        if config is None:
            return load_yaml_obj(types.DEFAULT, 'azure', kind)
        return config        

