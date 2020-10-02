import os
import copy

from cli.version import VERSION
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_ansible_path, get_ansible_path_for_build, get_ansible_vault_path, MANIFEST_FILE_NAME
from cli.helpers.doc_list_helpers import select_first, select_single, ExpectedSingleResultException
from cli.helpers.naming_helpers import to_feature_name, to_role_name
from cli.helpers.ObjDict import ObjDict
from cli.helpers.yaml_helpers import dump
from cli.helpers.Config import Config
from cli.helpers.data_loader import load_yaml_obj, types, load_yamls_file, load_all_documents_from_folder

from cli.engine.schema.DefaultMerger import DefaultMerger


class AnsibleVarsGenerator(Step):

    def __init__(self, inventory_creator=None, inventory_upgrade=None):
        super().__init__(__name__)

        self.inventory_creator = inventory_creator
        self.inventory_upgrade = inventory_upgrade
        self.roles_with_generated_vars = []
        self.manifest_docs = []

        if inventory_creator != None and inventory_upgrade == None:
            self.cluster_model = inventory_creator.cluster_model
            self.config_docs = [self.cluster_model] + inventory_creator.config_docs
        elif inventory_upgrade != None and inventory_creator == None:
            self.cluster_model = inventory_upgrade.cluster_model
            self.config_docs = load_all_documents_from_folder('common', 'defaults/configuration')
            self.manifest_docs = self.get_manifest_docs()
        else:
            raise Exception('Invalid AnsibleVarsGenerator configuration')

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def generate(self):
        self.logger.info('Generate Ansible vars')
        self.is_upgrade_run = self.inventory_creator == None
        if self.is_upgrade_run:
            ansible_dir = get_ansible_path_for_build(self.inventory_upgrade.build_dir)
        else:
            ansible_dir = get_ansible_path(self.cluster_model.specification.name)

        cluster_config_file_path = os.path.join(ansible_dir, 'roles', 'common', 'vars', 'main.yml')
        clean_cluster_model = self.get_clean_cluster_model()
        with open(cluster_config_file_path, 'w') as stream:
            dump(clean_cluster_model, stream)

        if self.is_upgrade_run:
            # For upgrade at this point we don't need any of other roles then
            # common, upgrade, repository, image_registry, haproxy and node_exporter.
            # - commmon is already provisioned from the cluster model constructed from the inventory.
            # - upgrade should not require any additional config
            # roles in the list below are provisioned for upgrade from defaults
            enabled_roles = ['repository', 'image_registry', 'haproxy', 'node_exporter']
        else:
            enabled_roles = self.inventory_creator.get_enabled_roles()

        for role in enabled_roles:
            kind = 'configuration/' + to_feature_name(role)

            document = select_first(self.config_docs, lambda x: x.kind == kind)
            if document is None:
                self.logger.warn('No config document for enabled role: ' + role)
                continue

            document.specification['provider'] = self.cluster_model.provider
            self.write_role_vars(ansible_dir, role, document)
            self.write_role_manifest_vars(ansible_dir, role, kind)

        self.populate_group_vars(ansible_dir)

    def write_role_vars(self, ansible_dir, role, document, vars_file_name='main.yml'):
        vars_dir = os.path.join(ansible_dir, 'roles', to_role_name(role), 'vars')
        if not os.path.exists(vars_dir):
            os.makedirs(vars_dir)

        vars_file_path = os.path.join(vars_dir, vars_file_name)

        with open(vars_file_path, 'w') as stream:
            dump(document, stream)

        if vars_file_name == 'main.yml':
            self.roles_with_generated_vars.append(to_role_name(role))

    def write_role_manifest_vars(self, ansible_dir, role, kind):
        enabled_kinds = {"configuration/haproxy", "configuration/node-exporter"}

        if kind not in enabled_kinds:
            return  # skip

        try:
            cluster_model = select_single(self.manifest_docs, lambda x: x.kind == 'epiphany-cluster')
        except ExpectedSingleResultException:
            return  # skip

        document = select_first(self.manifest_docs, lambda x: x.kind == kind)
        if document is None:
            # If there is no document provided by the user, then fallback to defaults
            document = load_yaml_obj(types.DEFAULT, 'common', kind)
            # Inject the required "version" attribute
            document['version'] = VERSION

        # Copy the "provider" value from the cluster model
        document['provider'] = cluster_model['provider']

        # Merge the document with defaults
        with DefaultMerger([document]) as doc_merger:
            document = doc_merger.run()[0]

        self.write_role_vars(ansible_dir, role, document, vars_file_name='manifest.yml')

    def populate_group_vars(self, ansible_dir):
        main_vars = ObjDict()
        main_vars['admin_user'] = self.cluster_model.specification.admin_user
        main_vars['k8s_as_cloud_service'] = self.cluster_model.specification.cloud.k8s_as_cloud_service
        main_vars['validate_certs'] = Config().validate_certs
        main_vars['offline_requirements'] = Config().offline_requirements
        main_vars['wait_for_pods'] = Config().wait_for_pods
        main_vars['is_upgrade_run'] = self.is_upgrade_run
        main_vars['roles_with_generated_vars'] = sorted(self.roles_with_generated_vars)

        if self.is_upgrade_run:
            shared_config_doc = self.get_shared_config_from_manifest()
        else:
            shared_config_doc = select_first(self.config_docs, lambda x: x.kind == 'configuration/shared-config')

        # Fallback if there is completely no trace of the shared-config doc
        if shared_config_doc is None:
            shared_config_doc = load_yaml_obj(types.DEFAULT, 'common', 'configuration/shared-config')

        self.set_vault_path(shared_config_doc)
        main_vars.update(shared_config_doc.specification)

        vars_dir = os.path.join(ansible_dir, 'group_vars')
        if not os.path.exists(vars_dir):
            os.makedirs(vars_dir)

        vars_file_name = 'all.yml'
        vars_file_path = os.path.join(vars_dir, vars_file_name)

        with open(vars_file_path, 'a') as stream:
            dump(main_vars, stream)

    def set_vault_path(self, shared_config):
        if shared_config.specification.vault_location == '':
            shared_config.specification.vault_tmp_file_location = Config().vault_password_location
            cluster_name = self.get_cluster_name()
            shared_config.specification.vault_location = get_ansible_vault_path(cluster_name)

    def get_cluster_name(self):
        if 'name' in self.cluster_model.specification.keys():
            return self.cluster_model.specification.name
        elif self.inventory_upgrade is not None:
            return os.path.basename(self.inventory_upgrade.build_dir)
        return 'default'

    def get_clean_cluster_model(self):
        cluster_model = copy.copy(self.cluster_model)
        self.clear_object(cluster_model, 'credentials')
        return cluster_model

    def get_manifest_docs(self):
        path_to_manifest = os.path.join(self.inventory_upgrade.build_dir, MANIFEST_FILE_NAME)
        if not os.path.isfile(path_to_manifest):
            raise Exception('No manifest.yml inside the build folder')

        manifest_docs = load_yamls_file(path_to_manifest)
        return manifest_docs

    def get_shared_config_from_manifest(self):
        # Reuse shared config from existing manifest
        # Shared config contains the use_ha_control_plane flag which is required during upgrades

        cluster_model = select_single(self.manifest_docs, lambda x: x.kind == 'epiphany-cluster')

        try:
            shared_config_doc = select_single(self.manifest_docs, lambda x: x.kind == 'configuration/shared-config')
            shared_config_doc['provider'] = cluster_model['provider']
        except ExpectedSingleResultException:
            # If there is no shared-config doc inside the manifest file, this is probably a v0.3 cluster
            # Returning None here (there is nothing to merge at this point) and
            # hoping that the shared-config doc from defaults will be enough
            return None

        # Merge the shared config doc with defaults
        with DefaultMerger([shared_config_doc]) as doc_merger:
            shared_config_doc = doc_merger.run()[0]
            del shared_config_doc['provider']

        return shared_config_doc

    def clear_object(self, obj_to_clean, key_to_clean):
        for key, val in obj_to_clean.items():
            if key == key_to_clean:
                obj_to_clean[key] = ''
                continue
            if isinstance(obj_to_clean[key], ObjDict):
                self.clear_object(obj_to_clean[key], key_to_clean)
