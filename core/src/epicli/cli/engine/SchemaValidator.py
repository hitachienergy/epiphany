import cli.helpers.data_types as data_types
from jsonschema import validate
from cli.helpers.data_loader import load_all_data_files
from cli.helpers.objdict_helpers import objdict_to_dict
from helpers.Step import Step


class SchemaValidator(Step):
    def __init__(self, cluster_model, docs):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.docs = docs

    def run(self):
        for doc in self.docs:
            schemas = load_all_data_files(data_types.VALIDATION, self.cluster_model.provider, doc.kind)

            if len(schemas) > 0:
                self.logger.info("Validating: " + doc.kind)
                validate(instance=objdict_to_dict(doc), schema=objdict_to_dict(schemas[0]))
            else:
                self.logger.warning("No validation schema for kind: " + doc.kind)

