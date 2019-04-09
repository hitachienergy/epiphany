from jsonschema import validate
from cli.helpers.data_loader import load_yaml_obj, types
from cli.helpers.objdict_helpers import objdict_to_dict, dict_to_objdict
from cli.helpers.Step import Step
from copy import deepcopy


class SchemaValidator(Step):
    def __init__(self, cluster_model, docs):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.docs = docs

        base = load_yaml_obj(types.VALIDATION, self.cluster_model.provider, 'core/base')
        definitions = load_yaml_obj(types.VALIDATION, self.cluster_model.provider, 'core/definitions')

        self.base_schema = dict_to_objdict(deepcopy(base))
        self.base_schema['definitions'] = definitions

        self.base_schema_no_provider = dict_to_objdict(deepcopy(base))
        self.base_schema_no_provider['definitions'] = definitions
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

    def run(self):
        for doc in self.docs:
            schema = self.get_base_schema(doc.kind)
            schema["specification"] = load_yaml_obj(types.VALIDATION, self.cluster_model.provider, doc.kind)
            self.logger.info("Validating: " + doc.kind)
            validate(instance=objdict_to_dict(doc), schema=objdict_to_dict(schema))

