import os

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_inventory_path_for_build, check_build_output_version, BUILD_LEGACY
from cli.models.AnsibleHostModel import AnsibleHostModel
from cli.models.AnsibleInventoryItem import AnsibleInventoryItem
from cli.helpers.build_saver import save_inventory
from cli.helpers.objdict_helpers import dict_to_objdict
from cli.helpers.data_loader import load_yamls_file, load_yaml_obj, types as data_types
from cli.helpers.doc_list_helpers import select_single
from cli.helpers.objdict_helpers import merge_objdict
from cli.helpers.data_loader import load_manifest_docs


class AnsibleInventoryUpgrade(Step):
    def __init__(self, build_dir, backup_build_dir):
        super().__init__(__name__)
        self.build_dir = build_dir
        self.backup_build_dir = backup_build_dir
        self.cluster_model = None
        self.manifest_docs = []

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)   

    def get_role(self, inventory, role_name):
        for role in inventory:
            if role.role == role_name:
                return role
        return None

    def delete_role(self, inventory, role_name):
        for i in range(len(inventory)):
            if inventory[i].role == role_name:
                del inventory[i]
                return       

    def rename_role(self, inventory, role_name, new_role_name):
        role = self.get_role(inventory, role_name)
        if role != None:
            role.role = new_role_name

    def upgrade(self):
        inventory_path = get_inventory_path_for_build(self.backup_build_dir)  
        build_version = check_build_output_version(self.backup_build_dir)

        self.logger.info(f'Loading backup Ansible inventory: {inventory_path}')
        loaded_inventory = InventoryManager(loader = DataLoader(), sources=inventory_path)

        # move loaded inventory to templating structure
        new_inventory = []
        for key in loaded_inventory.groups:
            if key != 'all' and  key != 'ungrouped':
                group_hosts = loaded_inventory.groups[key].hosts
                new_hosts = []
                for host in group_hosts:
                    new_hosts.append(AnsibleHostModel(host.address, host.vars['ansible_host']))
                new_inventory.append(AnsibleInventoryItem(key, new_hosts))

        if build_version == BUILD_LEGACY:
            self.logger.info(f'Upgrading Ansible inventory Epiphany < 0.3.0')

            # Epiphany < 0.3.0 did not have manifest file in build folder so lets create bare minimum cluster model from inventory
            self.cluster_model = dict_to_objdict({
                'provider': 'any',
                'specification': {
                    'admin_user': {
                        'name': loaded_inventory.groups['all'].vars['ansible_user'],
                        'key_path': loaded_inventory.groups['all'].vars['ansible_ssh_private_key_file']
                    }
                }
            })

            # Remap roles
            self.rename_role(new_inventory, 'master', 'kubernetes_master')
            self.rename_role(new_inventory, 'worker', 'kubernetes_node')
            self.rename_role(new_inventory, 'deployments', 'applications')
            self.rename_role(new_inventory, 'elasticsearch-curator', 'elasticsearch_curator')
            self.rename_role(new_inventory, 'jmx-exporter', 'jmx_exporter')
            self.rename_role(new_inventory, 'kafka-exporter', 'kafka_exporter')
            self.rename_role(new_inventory, 'haproxy_tls_termination', 'haproxy')

            # remove linux and reboot roles if present
            self.delete_role(new_inventory, 'linux')
            self.delete_role(new_inventory, 'reboot')
        else:
            self.logger.info(f'Upgrading Ansible inventory Epiphany => 0.3.0')

            # load cluster model from manifest
            self.manifest_docs = load_manifest_docs(self.backup_build_dir)
            self.cluster_model = select_single(self.manifest_docs, lambda x: x.kind == 'epiphany-cluster')

        # Merge manifest cluster config with newer defaults
        default_cluster_model = load_yaml_obj(data_types.DEFAULT, 'common', 'epiphany-cluster')
        merge_objdict(default_cluster_model, self.cluster_model)
        self.cluster_model = default_cluster_model

        # repository & image_registry roles added in v0.4.0
        repository = self.get_role(new_inventory, 'repository')
        if repository is None:
            raise Exception('repository group not found in inventory. '
                            'Your deployment may not be supported by this version of Epiphany. '
                            'You may try to use older version first.')

        # add image_registry if not present
        image_registry = self.get_role(new_inventory, 'image_registry')
        if image_registry is None:
            hosts = [AnsibleHostModel(repository.hosts[0].name, repository.hosts[0].ip)]
            new_inventory.append(AnsibleInventoryItem('image_registry', hosts))

        # save new inventory
        save_inventory(new_inventory, self.cluster_model, self.build_dir)

        return 0
