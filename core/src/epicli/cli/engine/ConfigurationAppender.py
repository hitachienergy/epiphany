import cli.helpers.data_types as data_types
from cli.helpers.data_loader import load_data_file
from cli.helpers.config_merger import merge_with_defaults
from cli.helpers.doc_list_helpers import select_first
from cli.engine.Step import Step


class ConfigurationAppender(Step):
    def __init__(self, cluster_model, docs):
        Step.__init__(self, __name__)
        self.cluster_model = cluster_model
        self.docs = docs

    def run(self):
        for component_key, component_value in self.cluster_model.specification.components.items():
            if component_value.count < 1:
                continue

            features_map = select_first(self.docs, lambda x: x.kind == 'configuration/feature-mapping')
            if features_map is None:
                features_map = load_data_file(data_types.DEFAULT, 'common', 'configuration/feature-mapping')
                self.logger.info("Adding: " + features_map.kind)
                self.docs.append(features_map)

            config_selector = component_value.configuration
            for feature_key in features_map.specification[component_key]:
                config = select_first(self.docs, lambda x: x.kind == 'configuration/' + feature_key and x.name == config_selector)
                if config is None:
                    config = merge_with_defaults('common', 'configuration/' + feature_key, config_selector)
                    self.logger.info("Adding: " + config.kind)
                self.docs.append(config)

