import cli.models.data_file_consts as model_constants
from cli.helpers.list_helpers import select_first
from cli.helpers.defaults_loader import load_all_docs_from_defaults
from cli.engine.dict_merge import merge_dict


def merge_with_defaults(provider, feature_kind, config_selector):
    files = load_all_docs_from_defaults(provider, feature_kind)
    config_spec = select_first(files, lambda x: x[model_constants.NAME] == config_selector)
    if config_selector != "default":
        default_config = select_first(files, lambda x: x[model_constants.NAME] == "default")
        merge_dict(default_config, config_spec)
        return default_config
    return config_spec
