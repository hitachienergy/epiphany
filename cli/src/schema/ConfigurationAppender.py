from typing import Callable, Dict, List

from cli.src.helpers.config_merger import merge_with_defaults
from cli.src.helpers.data_loader import load_schema_obj, schema_types
from cli.src.helpers.doc_list_helpers import select_first, select_single
from cli.src.Step import Step
from cli.version import VERSION


class ConfigurationAppender(Step):
    REQUIRED_DOCS = ['epiphany-cluster',
                     'configuration/features',
                     'configuration/feature-mappings',
                     'configuration/shared-config']

    def __init__(self, input_docs):
        super().__init__(__name__)
        self.__cluster_model: Dict = select_single(input_docs, lambda x: x.kind == 'epiphany-cluster')
        self.__input_docs: List[Dict] = input_docs

    def __append_config(self, config_docs: List[Dict], document: Dict):
        document['version'] = VERSION
        config_docs.append(document)

    def __add_doc(self, config_docs: List[Dict], document_kind: str):
        doc = select_first(self.__input_docs, lambda x, kind=document_kind: x.kind == kind)
        if doc is None:
            doc = load_schema_obj(schema_types.DEFAULT, 'common', document_kind)
            self.logger.info(f'Adding: {doc.kind}')

        self.__append_config(config_docs, doc)

    def __feature_selector(self, feature_key: str, config_selector: str) -> Callable:
        return lambda x, key=feature_key, selector=config_selector: x.kind == f'configuration/{key}' and x.name == selector

    def add_feature_mappings(self):
        feature_mappings: List[Dict] = []
        self.__add_doc(feature_mappings, 'configuration/feature-mappings')

        if feature_mappings is not None:
            self.__input_docs.append(feature_mappings[0])

    def run(self):
        configuration_docs: List[Dict] = []

        for document_kind in ConfigurationAppender.REQUIRED_DOCS:
            self.__add_doc(configuration_docs, document_kind)

        for component_key, component_value in self.__cluster_model.specification.components.items():
            if component_value.count < 1:
                continue

            feature_mappings = select_first(configuration_docs, lambda x: x.kind == 'configuration/feature-mappings')
            config_selector = component_value.configuration
            for feature_key in feature_mappings.specification.mappings[component_key]:
                first_input_docs_config = select_first(self.__input_docs, self.__feature_selector(feature_key, config_selector))
                if first_input_docs_config is not None:
                    self.__append_config(configuration_docs, first_input_docs_config)
                else:
                    first_config = select_first(configuration_docs, self.__feature_selector(feature_key, config_selector))

                    if first_config is None:
                        merged_config = merge_with_defaults('common', f'configuration/{feature_key}', config_selector, self.__input_docs)
                        self.logger.info(f'Adding: {merged_config.kind}')
                        self.__append_config(configuration_docs, merged_config)

        return configuration_docs
