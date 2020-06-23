from jsonschema import validate
from cli.helpers.data_loader import load_yaml_obj, types
from cli.helpers.objdict_helpers import objdict_to_dict, dict_to_objdict
from cli.helpers.Step import Step
from copy import deepcopy
from cli.helpers.doc_list_helpers import select_single


class SchemaValidator(Step):
    def __init__(self, cluster_model, validation_docs):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.validation_docs = validation_docs

        base = load_yaml_obj(types.VALIDATION, self.cluster_model.provider, 'core/base')
        self.definitions = load_yaml_obj(types.VALIDATION, self.cluster_model.provider, 'core/definitions')

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

    def run_for_individual_documents(self):
        for doc in self.validation_docs:
            # Load document schema
            schema = load_yaml_obj(types.VALIDATION, self.cluster_model.provider, doc.kind)

            # Include "definitions"
            schema['definitions'] = self.definitions

            # Warn the user about the missing validation
            if hasattr(schema, '$ref'):
                if schema['$ref'] == '#/definitions/unvalidated_specification':
                    self.logger.warn('No specification validation for ' + doc.kind)

            # Assert the schema
            try:
                validate(instance=objdict_to_dict(doc), schema=objdict_to_dict(schema))
            except Exception as e:
                self.logger.error(f'Failed validating: {doc.kind}')
                self.logger.error(e)
                raise Exception('Schema validation error, see the error above.')

    def run(self):
        for doc in self.validation_docs:
            self.logger.info(f'Validating: {doc.kind}')
            schema = self.get_base_schema(doc.kind)
            schema['properties']['specification'] = load_yaml_obj(types.VALIDATION, self.cluster_model.provider, doc.kind)
            if hasattr(schema['properties']["specification"], '$ref'):
                if schema['properties']["specification"]['$ref'] == '#/definitions/unvalidated_specification':
                    self.logger.warn('No specification validation for ' + doc.kind)
            try:
                validate(instance=objdict_to_dict(doc), schema=objdict_to_dict(schema))
            except Exception as e:
                self.logger.error(f'Failed validating: {doc.kind}')
                self.logger.error(e)
                raise Exception('Schema validation error, see the error above.')
