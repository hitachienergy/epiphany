from pathlib import Path

from cli.src.Step import Step
from cli.src.helpers.build_io import get_inventory_path_for_build, load_inventory, save_inventory
from cli.src.helpers.data_loader import load_schema_obj, schema_types
from cli.src.helpers.objdict_helpers import merge_objdict
from cli.src.models.AnsibleHostModel import AnsibleHostModel
from cli.src.models.AnsibleInventoryItem import AnsibleInventoryItem
from cli.src.schema.ManifestHandler import ManifestHandler


class AnsibleInventoryUpgrade(Step):
    def __init__(self, build_dir, backup_build_dir, config_docs):
        super().__init__(__name__)
        self.build_dir = build_dir
        self.backup_build_dir = backup_build_dir
        self.cluster_model = None
        self.config_docs = config_docs
        self.mhandler: ManifestHandler = ManifestHandler(build_path=Path(build_dir))

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
        if role is not None:
            role.role = new_role_name

    def get_new_config_roles(self):
        roles = []
        for doc in self.config_docs:
            if "configuration/" in doc.kind:
                roles.append(doc.kind.replace('configuration/', ''))
        return roles

    def upgrade(self):
        inventory_path = get_inventory_path_for_build(self.backup_build_dir)

        self.logger.info(f'Loading backup Ansible inventory: {inventory_path}')
        loaded_inventory = load_inventory(inventory_path)

        # move loaded inventory to templating structure
        new_inventory = []
        for key in loaded_inventory.groups:
            if key != 'all' and  key != 'ungrouped':
                group_hosts = loaded_inventory.groups[key].hosts
                new_hosts = []
                for host in group_hosts:
                    new_hosts.append(AnsibleHostModel(host.address, host.vars['ansible_host']))
                new_inventory.append(AnsibleInventoryItem(key, new_hosts))

        self.logger.info('Upgrading Ansible inventory')

        # load cluster model from manifest
        self.mhandler = ManifestHandler(build_path=Path(self.backup_build_dir))
        self.mhandler.read_manifest()
        self.cluster_model = self.mhandler.cluster_model

        # Merge manifest cluster config with newer defaults
        default_cluster_model = load_schema_obj(schema_types.DEFAULT, self.cluster_model.provider, 'epiphany-cluster')
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
