import yaml
from cli.helpers.ObjDict import ObjDict


def nested_dict_to_objdict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            nested_dict_to_objdict(v)
            d[k] = ObjDict(v)


def nested_objdict_to_dict(d):
    for k, v in d.items():
        if isinstance(v, ObjDict):
            nested_objdict_to_dict(v)
            d[k] = dict(v)


def safe_load_all(stream):
    docs = list(yaml.safe_load_all(stream))
    conv_docs = []
    for doc in docs:
        nested_dict_to_objdict(doc)
        conv_docs.append(ObjDict(doc))
    return conv_docs


def safe_load(stream):
    doc = yaml.safe_load(stream)
    nested_dict_to_objdict(doc)
    return ObjDict(doc)


def dump_all(docs, stream, default_flow_style=False):
    conv_docs = []
    for doc in docs:
        nested_objdict_to_dict(doc)
        conv_docs.append(dict(doc))
    yaml.dump_all(conv_docs, stream, default_flow_style=False)
