import logging
import cli.helpers.data_types as data_types
from jsonschema import validate
from cli.helpers.data_loader import load_all_data_files
from cli.helpers.objdict_helpers import objdict_to_dict


class SchemaValidator:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def validate(self, docs, provider):
        self.logger.info("Running schema validator")
        for doc in docs:
            schemas = load_all_data_files(data_types.VALIDATION, provider, doc.kind)

            if len(schemas) > 0:
                self.logger.info("Validating: " + doc.kind)
                validate(instance=objdict_to_dict(doc), schema=objdict_to_dict(schemas[0]))
            else:
                self.logger.warning("No validation schema for kind: " + doc.kind)

        self.logger.info("Done validating\n")

