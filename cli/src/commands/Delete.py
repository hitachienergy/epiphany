from pathlib import Path

from cli.src.Step import Step
from cli.src.helpers.build_io import delete_directory
from cli.src.schema.ManifestHandler import ManifestHandler
from cli.src.terraform.TerraformRunner import TerraformRunner


class Delete(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.build_directory = input_data.build_directory

    def delete(self):
        mhandler = ManifestHandler(build_path=Path(self.build_directory))
        mhandler.read_manifest()
        cluster_model = mhandler.cluster_model

        if cluster_model['provider'] == 'any':
            raise Exception('Delete works only for cloud providers')

        with TerraformRunner(cluster_model, mhandler.docs) as tf_runner:
            tf_runner.destroy()

        delete_directory(self.build_directory)

        return 0
