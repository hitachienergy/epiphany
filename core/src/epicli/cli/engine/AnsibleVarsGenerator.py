import os
import glob
import shutil

from cli.helpers.Step import Step
from cli.helpers.build_saver import save_to_file, get_ansible_path
from cli.helpers.data_loader import load_template_file, types


class AnsibleVarsGenerator(Step):

    def __init__(self, cluster_model, infrastructure):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.infrastructure = [cluster_model] + infrastructure

    def run(self):
        ansible_dir = get_ansible_path(self.cluster_model.specification.name)
        ansible_main_file_path = os.path.join(ansible_dir, "main.yml")

        template = load_template_file(types.ANSIBLE, "common", "main.yml")
        content = template.render(cluster_model=self.cluster_model)
        self.logger.info(str(content))

        save_to_file(ansible_main_file_path, content)

        for filename in glob.iglob(os.path.join(ansible_dir, "roles", "*")):
            vars_dir = os.path.join(filename, "vars")
            if not os.path.exists(vars_dir):
                os.makedirs(vars_dir)

            shutil.copy(ansible_main_file_path, vars_dir)
