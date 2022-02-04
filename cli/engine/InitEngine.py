import os

from cli.helpers.Step import Step
from cli.helpers.build_io import save_manifest, get_build_path
from cli.helpers.data_loader import load_all_schema_objs, types
from cli.helpers.objdict_helpers import remove_value
from cli.version import VERSION
from cli.helpers.doc_list_helpers import select_all
from cli.engine.schema.ConfigurationAppender import ConfigurationAppender
from cli.engine.schema.DefaultMerger import DefaultMerger


class InitEngine(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.provider = input_data.provider
        self.full_config = input_data.full_config
        self.name = input_data.name
        self.is_full_config = input_data.full_config

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def init(self):
        # Load the minimal cluster-config doc and set the cluster name
        docs = load_all_schema_objs(types.DEFAULT, self.provider, 'configuration/minimal-cluster-config')
        docs[0].specification.name = self.name

        # For full we also add the infrastructure and configuration documents
        if self.is_full_config:
            # Merge with defaults
            with DefaultMerger(docs) as doc_merger:
                    docs = doc_merger.run()

            # Add infrastructure and configuration documents
            if self.provider != 'any':
                # Add VM infrastructure docs as these are most likely to be changed
                infra_docs = load_all_schema_objs(types.DEFAULT, self.provider, 'infrastructure/virtual-machine')
            else:
                # For any provider, infrastructure docs are already part of the minimal-cluster-config template
                infra_docs = select_all(docs, lambda x: x.kind.startswith('infrastructure/machine'))

            # Add configuration documents
            with ConfigurationAppender(docs) as config_appender:
                config_docs = config_appender.run()

            docs = [*config_docs, *infra_docs]

        # set the provider and version for all docs
        for doc in docs:
            doc['provider'] = self.provider
            doc['version'] = VERSION

        # remove SET_BY_AUTOMATION fields
        remove_value(docs, 'SET_BY_AUTOMATION')

        # save document
        save_manifest(docs, self.name, f'{ self.name }.yml')

        self.logger.info('Initialized new configuration and saved it to "' + os.path.join(get_build_path(self.name), self.name + '.yml') + '"')
        return 0
