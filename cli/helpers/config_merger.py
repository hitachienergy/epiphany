from copy import deepcopy

from cli.helpers.doc_list_helpers import select_first
from cli.helpers.data_loader import load_all_schema_objs, types
from cli.helpers.objdict_helpers import merge_objdict, dict_to_objdict
from cli.version import VERSION


def merge_with_defaults(provider, feature_kind, config_selector, docs):
    files = load_all_schema_objs(types.DEFAULT, provider, feature_kind)
    config_spec = select_first(files, lambda x: x.name == config_selector)
    if config_selector != 'default':
        default_config = dict_to_objdict(deepcopy(select_first(docs, lambda x: x.name == 'default' and x.kind == feature_kind)))
        default_doc = select_first(files, lambda x: x.name == 'default')
        if default_config is not None:
            merge_objdict(default_doc, default_config)
        merge_objdict(default_doc, config_spec)
        default_doc['version'] = VERSION
        return default_doc
    return config_spec
