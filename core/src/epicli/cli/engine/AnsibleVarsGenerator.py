import os

from cli.helpers.Step import Step
from cli.helpers.build_saver import get_ansible_path
from cli.helpers.doc_list_helpers import select_first
from cli.helpers.naming_helpers import to_feature_name, to_role_name
from cli.helpers.ObjDict import ObjDict
from cli.helpers.yaml_helpers import dump
import copy


class AnsibleVarsGenerator(Step):

    def __init__(self, cluster_model, infrastructure, inventory_creator):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = [cluster_model] + infrastructure
        self.inventory_creator = inventory_creator

    def run(self):
        enabled_roles = self.inventory_creator.get_enabled_roles()

        ansible_dir = get_ansible_path(self.cluster_model.specification.name)

        cluster_config_file_path = os.path.join(ansible_dir, 'roles', 'common', 'vars', 'main.yml')
        clean_cluster_model = self.get_clean_cluster_model()
        self.populate_group_vars(ansible_dir)
        with open(cluster_config_file_path, 'w') as stream:
            dump(clean_cluster_model, stream)

        for role in enabled_roles:
            document = select_first(self.config_docs, lambda x: x.kind == 'configuration/'+to_feature_name(role))

            if document is None:
                self.logger.warn('No config document for enabled role: ' + role)
                continue

            document = self.add_provider_info(document)
            vars_dir = os.path.join(ansible_dir, 'roles', to_role_name(role), 'vars')
            if not os.path.exists(vars_dir):
                os.makedirs(vars_dir)

            vars_file_name = 'main.yml'
            vars_file_path = os.path.join(vars_dir, vars_file_name)

            with open(vars_file_path, 'w') as stream:
                dump(document, stream)

    def populate_group_vars(self, ansible_dir):
        main_vars = ObjDict()
        main_vars = self.add_admin_user_name(main_vars)

        vars_dir = os.path.join(ansible_dir, 'group_vars')
        if not os.path.exists(vars_dir):
            os.makedirs(vars_dir)

        vars_file_name = 'all.yml'
        vars_file_path = os.path.join(vars_dir, vars_file_name)

        with open(vars_file_path, 'w') as stream:
            dump(main_vars, stream)

    def add_admin_user_name(self, document):
        if document is None:
            raise Exception('Config is empty for: ' + 'group_vars/all.yml')

        document['admin_user'] = self.cluster_model.specification.admin_user
        return document

    def add_provider_info(self, document):
        document.specification['provider'] = self.cluster_model.provider
        return document

    def get_clean_cluster_model(self):
        cluster_model = copy.copy(self.cluster_model)
        self.clear_object(cluster_model, 'credentials')
        return cluster_model

    def clear_object(self, obj_to_clean, key_to_clean):
        for key, val in obj_to_clean.items():
            if key == key_to_clean:
                obj_to_clean[key] = ''
                continue
            if isinstance(obj_to_clean[key], ObjDict):
                self.clear_object(obj_to_clean[key], key_to_clean)
