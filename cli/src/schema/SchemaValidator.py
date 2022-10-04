from copy import deepcopy

from jsonschema import Draft7Validator, validate

from cli.src.helpers.data_loader import load_schema_obj, schema_types
from cli.src.helpers.objdict_helpers import (dict_to_objdict, objdict_to_dict,
                                             replace_yesno_with_booleans)
from cli.src.Step import Step


class SchemaValidator(Step):
    def __init__(self, provider, validation_docs):
        super().__init__(__name__)
        self.provider = provider
        self.validation_docs = validation_docs

        base = load_schema_obj(schema_types.VALIDATION, self.provider, 'core/base')
        self.definitions = load_schema_obj(schema_types.VALIDATION, self.provider, 'core/definitions')

        self.base_schema = dict_to_objdict(deepcopy(base))
        self.base_schema['definitions'] = self.definitions

        self.base_schema_no_provider = dict_to_objdict(deepcopy(base))
        self.base_schema_no_provider['definitions'] = self.definitions
        del self.base_schema_no_provider.required[0]
        del self.base_schema_no_provider.properties['provider']

    def get_base_schema(self, kind):
        if 'infrastructure' in kind or kind == 'epiphany-cluster':
            schema = self.base_schema
        else:
            schema = self.base_schema_no_provider
        schema.properties.kind.default = kind
        schema.properties.kind.pattern = '^(' + kind + ')$'
        return schema

    def validate_document(self, doc, schema):
        try:
            replace_yesno_with_booleans(doc)
            Draft7Validator.check_schema(schema)
            validate(instance=objdict_to_dict(doc), schema=schema)
        except Exception as e:
            self.logger.error(f'Failed validating: {doc.kind}')
            self.logger.error(e)
            raise Exception('Schema validation error, see the error above.') from e

    def run_for_individual_documents(self):
        for doc in self.validation_docs:
            # Load document schema
            schema = load_schema_obj(schema_types.VALIDATION, self.provider, doc.kind)

            # Include "definitions"
            schema['definitions'] = self.definitions

            # Warn the user about the missing validation
            if hasattr(schema, '$ref'):
                if schema['$ref'] == '#/definitions/unvalidated_specification':
                    self.logger.warn('No specification validation for ' + doc.kind)

            # Assert the schema
            schema_dict = objdict_to_dict(schema)
            self.validate_document(doc, schema_dict)

    def run(self):
        for doc in self.validation_docs:
            schema = self.get_base_schema(doc.kind)
            schema['properties']['specification'] = load_schema_obj(schema_types.VALIDATION, self.provider, doc.kind)
            if hasattr(doc["specification"], 'name'):
                name = doc["specification"]["name"]
                self.logger.info(f'Validating: {doc.kind} - {name}')
            else:
                self.logger.info(f'Validating: {doc.kind}')
            if hasattr(schema['properties']["specification"], '$ref'):
                if schema['properties']["specification"]['$ref'] == '#/definitions/unvalidated_specification':
                    self.logger.warn('No specification validation for ' + doc.kind)
            schema_dict = objdict_to_dict(schema)
            self.validate_document(doc, schema_dict)
