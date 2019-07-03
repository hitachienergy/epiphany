
from cli.helpers.build_saver import save_manifest
from cli.helpers.data_loader import load_all_yaml_objs, types, load_all_documents_from_folder
from cli.engine.EpiphanyEngine import EpiphanyEngine


class UserConfigInitializer:
    def __init__(self, input_data):
        self.provider = input_data.provider
        self.full_config = input_data.full_config
        self.name = input_data.name
        self.is_full_config = input_data.full_config

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        defaults = load_all_yaml_objs(types.DEFAULT, self.provider, 'configuration/minimal-cluster-config')
        defaults[0].specification.name = self.name

        if self.is_full_config:
            defaults = self.get_full_config(defaults)

        save_manifest(defaults, self.name, self.name+'.yml')

    def get_full_config(self, config_docs):
        cluster_config_path = save_manifest(config_docs, self.name, self.name + '.yml')
        args = type('obj', (object,), {'file': cluster_config_path})()
        with EpiphanyEngine(args) as engine:
            config_docs = engine.dry_run()

        infra_docs = load_all_documents_from_folder(self.provider, 'defaults/infrastructure')
        return [*config_docs, *infra_docs]
