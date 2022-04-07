from cli.src.helpers.build_io import delete_directory, load_manifest
from cli.src.helpers.cli_helpers import query_yes_no
from cli.src.helpers.doc_list_helpers import select_single
from cli.src.Step import Step
from cli.src.terraform.TerraformRunner import TerraformRunner


class Delete(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.build_directory = input_data.build_directory

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def delete(self):
        docs = load_manifest(self.build_directory)
        cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')

        if cluster_model.provider == 'any':
            raise Exception('Delete works only for cloud providers')

        if cluster_model.provider == 'azure':
            if not query_yes_no("Terraform will delete existing cluster with all disks belonging to parent Resource Group."
                                "Do you want to continue?"):
                sys.exit(0)

        with TerraformRunner(cluster_model, docs) as tf_runner:
            tf_runner.destroy()

        delete_directory(self.build_directory)

        return 0
