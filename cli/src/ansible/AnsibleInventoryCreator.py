from collections import defaultdict

from cli.src.helpers.build_io import save_inventory
from cli.src.helpers.doc_list_helpers import select_single
from cli.src.helpers.naming_helpers import to_role_name
from cli.src.models.AnsibleInventoryItem import AnsibleInventoryItem
from cli.src.providers.provider_class_loader import provider_class_loader
from cli.src.Step import Step


class AnsibleInventoryCreator(Step):
    def __init__(self, cluster_model, config_docs):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.proxy = self.get_proxy()

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # todo: add login for ansible
    def create(self):
        self.logger.info('Creating Ansible inventory')
        inventory = self.get_inventory()
        save_inventory(inventory, self.cluster_model)

    def get_inventory(self):
        inventory = []
        for component_key, component_value in self.cluster_model.specification.components.items():
            if component_value.count < 1:
                continue
            ips = self.proxy.get_ips_for_feature(component_key)
            if len(ips) > 0:
                roles = self.get_roles_for_feature(component_key)
                for role in roles:
                    ansible_role_name = to_role_name(role)
                    inventory.append(AnsibleInventoryItem(ansible_role_name, ips))

        return self.group_duplicated(inventory)

    def get_roles_for_feature(self, component_key):
        features_map = select_single(self.config_docs, lambda x: x.kind == 'configuration/feature-mapping')
        return features_map.specification.roles_mapping[component_key]

    def get_available_roles(self):
        features_map = select_single(self.config_docs, lambda x: x.kind == 'configuration/feature-mapping')
        return features_map.specification.available_roles

    def get_enabled_roles(self):
        roles = self.get_available_roles()
        return [role["name"] for role in roles if role["enabled"]]

    def get_proxy(self):
        apiproxy = provider_class_loader(self.cluster_model.provider, 'APIProxy')
        return apiproxy(self.cluster_model, self.config_docs)

    @staticmethod
    def group_duplicated(inventory):
        groups = defaultdict(list)
        for item in inventory:
            for host in item.hosts:
                if host not in groups[item.role]:
                    groups[item.role].append(host)

        result = []
        for key, value in groups.items():
            result.append(AnsibleInventoryItem(key, value))
        return result
