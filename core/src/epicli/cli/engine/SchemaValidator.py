import logging
from cli.helpers.objdict_helpers import objdict_to_dict
from jsonschema import validate

schema = {
     "type" : "object",
     "properties" : {
         "number" : {"type" : "number"},
         "string" : {"type" : "string"},
     },
}

class SchemaValidator:

    def __init__(self, config_docs):
        self.config_docs = []
        for doc in config_docs:
            self.config_docs.append(objdict_to_dict(doc))
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def validate(self):
        validate(instance={"number": 1, "string": 'string'}, schema=schema)
