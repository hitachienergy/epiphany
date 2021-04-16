from cli.helpers.doc_list_helpers import select_first
from cli.helpers.data_loader import load_all_yaml_objs, types
from cli.helpers.objdict_helpers import merge_objdict
from cli.version import VERSION


def merge_with_defaults(provider, feature_kind, config_selector, docs):
    files = load_all_yaml_objs(types.DEFAULT, provider, feature_kind)
    config_spec = select_first(files, lambda x: x.name == config_selector)
    if config_selector != 'default':
        default_config = select_first(docs, lambda x: x.name == 'default' and x.kind == feature_kind)
        if default_config is None:
            default_config = select_first(files, lambda x: x.name == 'default')
        default_config['version'] = VERSION
        merge_objdict(default_config, config_spec)
        return default_config
    return config_spec
