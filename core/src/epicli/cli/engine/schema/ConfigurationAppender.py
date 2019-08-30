from cli.helpers.data_loader import load_yaml_obj, types
from cli.helpers.config_merger import merge_with_defaults
from cli.helpers.doc_list_helpers import select_first
from cli.helpers.Step import Step
from cli.helpers.doc_list_helpers import select_single


class ConfigurationAppender(Step):
    def __init__(self, input_docs):
        super().__init__(__name__)
        self.cluster_model = select_single(input_docs, lambda x: x.kind == 'epiphany-cluster')
        self.input_docs = input_docs

    def run(self):
        configuration_docs = []

        for component_key, component_value in self.cluster_model.specification.components.items():
            if component_value.count < 1:
                continue

            features_map = select_first(self.input_docs, lambda x: x.kind == 'configuration/feature-mapping')
            if features_map is None:
                features_map = select_first(configuration_docs, lambda x: x.kind == 'configuration/feature-mapping')

            if features_map is None:
                features_map = load_yaml_obj(types.DEFAULT, 'common', 'configuration/feature-mapping')
                self.logger.info("Adding: " + features_map.kind)
                configuration_docs.append(features_map)

            config_selector = component_value.configuration
            for feature_key in features_map.specification.roles_mapping[component_key]:
                config = select_first(self.input_docs, lambda x: x.kind == 'configuration/' + feature_key and x.name == config_selector)
                if config is None:
                    config = select_first(configuration_docs, lambda
                        x: x.kind == 'configuration/' + feature_key and x.name == config_selector)
                if config is None:
                    config = merge_with_defaults('common', 'configuration/' + feature_key, config_selector)
                    self.logger.info("Adding: " + config.kind)
                    configuration_docs.append(config)

        return configuration_docs

