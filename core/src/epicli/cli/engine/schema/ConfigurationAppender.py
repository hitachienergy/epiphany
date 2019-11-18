from cli.helpers.data_loader import load_yaml_obj, types
from cli.helpers.config_merger import merge_with_defaults
from cli.helpers.doc_list_helpers import select_first
from cli.helpers.Step import Step
from cli.version import VERSION
from cli.helpers.doc_list_helpers import select_single


class ConfigurationAppender(Step):
    REQUIRED_DOCS = ['configuration/feature-mapping', 'configuration/shared-config', 'epiphany-cluster']

    def __init__(self, input_docs):
        super().__init__(__name__)
        self.cluster_model = select_single(input_docs, lambda x: x.kind == 'epiphany-cluster')
        self.input_docs = input_docs

    def run(self):
        configuration_docs = []

        def append_config(doc):
            doc['version'] = VERSION
            configuration_docs.append(doc)    

        for document_kind in ConfigurationAppender.REQUIRED_DOCS:
            doc = select_first(self.input_docs, lambda x: x.kind == document_kind)
            if doc is None:
                doc = load_yaml_obj(types.DEFAULT, 'common', document_kind)
                self.logger.info("Adding: " + doc.kind)
                append_config(doc)
            else:
                append_config(doc)

        for component_key, component_value in self.cluster_model.specification.components.items():
            if component_value.count < 1:
                continue

            features_map = select_first(configuration_docs, lambda x: x.kind == 'configuration/feature-mapping')
            config_selector = component_value.configuration
            for feature_key in features_map.specification.roles_mapping[component_key]:
                config = select_first(self.input_docs, lambda x: x.kind == 'configuration/' + feature_key and x.name == config_selector)
                if config is not None:
                    append_config(config)
                if config is None:
                    config = select_first(configuration_docs, lambda
                        x: x.kind == 'configuration/' + feature_key and x.name == config_selector)
                if config is None:
                    config = merge_with_defaults('common', 'configuration/' + feature_key, config_selector)
                    self.logger.info("Adding: " + config.kind)
                    append_config(config)

        return configuration_docs

