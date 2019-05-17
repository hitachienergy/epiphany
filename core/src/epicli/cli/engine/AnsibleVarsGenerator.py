import os
import glob
import shutil
import copy

from cli.helpers.Step import Step
from cli.helpers.build_saver import save_to_file, get_ansible_path
from cli.helpers.data_loader import load_template_file, types
from cli.helpers.doc_list_helpers import select_first, select_single
from cli.helpers.role_name_helper import to_feature_name, to_role_name
from cli.helpers.ObjDict import ObjDict
from cli.helpers.yaml_helpers import dump

class AnsibleVarsGenerator(Step):

    def __init__(self, cluster_model, infrastructure, inventory_creator):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = [cluster_model] + infrastructure
        self.inventory_creator = inventory_creator

    def run(self):
        enabled_roles = self.inventory_creator.get_enabled_roles()

        ansible_dir = get_ansible_path(self.cluster_model.specification.name)

        cluster_config_file_path = os.path.join(ansible_dir, "epiphany-cluster.yml")
        clean_cluster_model = self.get_clean_cluster_model()
        with open(cluster_config_file_path, 'w') as stream:
            dump(clean_cluster_model, stream)

        for role in enabled_roles:
            document = select_first(self.config_docs, lambda x: x.kind == 'configuration/'+to_feature_name(role))
            if document is None:
                self.logger.warn('No config document for enabled role: ' + role)
                continue

            vars_dir = os.path.join(ansible_dir, 'roles', to_role_name(role), 'vars')
            if not os.path.exists(vars_dir):
                os.makedirs(vars_dir)

            vars_file_name = to_feature_name(role)+'.yml'
            vars_file_path = os.path.join(vars_dir, vars_file_name)

            with open(vars_file_path, 'w') as stream:
                dump(document, stream)

            shutil.copy(cluster_config_file_path, vars_dir)

            vars_files = ['epiphany-cluster.yml', vars_file_name]

            main_vars_template = load_template_file(types.ANSIBLE, "common", "main.yml")
            content = main_vars_template.render(vars_files=vars_files)

            vars_main_file_path = os.path.join(vars_dir, 'main.yml')
            save_to_file(vars_main_file_path, content)

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


#todo dodaj generowanie z templatki inclide dla docukemtnu epiphany-cluster

        # ansible_main_file_path = os.path.join(ansible_dir, "main.yml")

        # template = load_template_file(types.ANSIBLE, "common", "main.yml")
        # content = template.render(cluster_model=self.cluster_model)
        # self.logger.info(str(content))

        # save_to_file(ansible_main_file_path, content)

        # for filename in glob.iglob(os.path.join(ansible_dir, "roles", "*")):
        #     vars_dir = os.path.join(filename, "vars")
        #     if not os.path.exists(vars_dir):
        #         os.makedirs(vars_dir)
        #
        #     shutil.copy(ansible_main_file_path, vars_dir)

