import yaml
from cli.helpers.objdict_helpers import objdict_to_dict, dict_to_objdict


def safe_load_all(stream):
    docs = list(yaml.safe_load_all(stream))
    conv_docs = []
    for doc in docs:
        conv_docs.append(dict_to_objdict(doc))
    return conv_docs


def safe_load(stream):
    doc = yaml.safe_load(stream)
    return dict_to_objdict(doc)


def dump_all(docs, stream):
    doc2 = docs
    conv_docs = []
    for doc in doc2:
        conv_docs.append(objdict_to_dict(doc))
    yaml.dump_all(conv_docs, stream, default_flow_style=False)


def dump(doc, stream):
    yaml.dump(objdict_to_dict(doc), stream, default_flow_style=False)

