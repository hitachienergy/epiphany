
import os
import sys

from cli.helpers.Step import Step
from cli.helpers.build_saver import save_manifest, get_build_path
from cli.helpers.data_loader import load_all_yaml_objs, types, load_all_documents_from_folder
from cli.engine.ApplyEngine import ApplyEngine
from cli.helpers.objdict_helpers import remove_value
from cli.version import VERSION
from cli.helpers.doc_list_helpers import select_all, select_single


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
        super().__exit__(exc_type, exc_value, traceback)  

    def init(self):
        input = load_all_yaml_objs(types.DEFAULT, self.provider, 'configuration/minimal-cluster-config')
        input[0].specification.name = self.name     

        if self.is_full_config:
            config = self.get_config_docs(input)
            config_only = select_all(config, lambda x: not(x.kind.startswith('epiphany-cluster')))
            if self.provider == 'any':
                # for any provider we want to use the default config from minimal-cluster-config
                cluster_model = select_single(input, lambda x: x.kind == 'epiphany-cluster')
            else:
                # for azure|aws provider we want to use the extended defaults cluster-config after dry run.
                # TODO: We probably wants this comming from seperate documents since Azure and AWS overlap now...
                cluster_model = select_single(config, lambda x: x.kind == 'epiphany-cluster')
            infra  = self.get_infra_docs(input)
            docs = [cluster_model, *config_only, *infra]
        else:
            docs = [*input]

        # set the provider and version for all docs
        for doc in docs:
            doc['provider'] = self.provider
            doc['version'] = VERSION  

        # remove SET_BY_AUTOMATION fields
        remove_value(docs, 'SET_BY_AUTOMATION')  

        # save document
        save_manifest(docs, self.name, self.name+'.yml')

        self.logger.info('Initialized new configuration and saved it to "' + os.path.join(get_build_path(self.name), self.name + '.yml') + '"')
        return 0

    def get_config_docs(self, input_docs):
        cluster_config_path = save_manifest(input_docs, self.name, self.name + '.yml')
        args = type('obj', (object,), {'file': cluster_config_path})()

        # generate the config documents
        with ApplyEngine(args) as build:
            config = build.dry_run() 
        
        return config

    def get_infra_docs(self, input_docs):
        if self.provider == 'any':
            # For any we can include the machine documents from the minimal-cluster-config
            infra = select_all(input_docs, lambda x: x.kind.startswith('infrastructure/machine'))
        else:
            # VMs are curently the infrastructure documents the user might interact with for:
            # - type/size
            # - distro
            # - network security rules
            # ...
            # So we add the defaults here.
            # TODO: Check if we want to include possible other infrastructure documents.           
            infra = load_all_yaml_objs(types.DEFAULT, self.provider, 'infrastructure/virtual-machine')
        
        return infra
