from ruamel.yaml import YAML
from cli.helpers.objdict_helpers import objdict_to_dict, dict_to_objdict


def safe_load_all(stream):
    yaml = YAML()
    yaml.default_flow_style = False     
    docs = list(yaml.load_all(stream))
    conv_docs = []
    for doc in docs:
        conv_docs.append(dict_to_objdict(doc))
    return conv_docs


def safe_load(stream):
    yaml = YAML()
    yaml.default_flow_style = False
    doc = yaml.load(stream)
    return dict_to_objdict(doc)


def dump_all(docs, stream):
    yaml = YAML()
    yaml.default_flow_style = False    
    doc2 = docs
    conv_docs = []
    for doc in doc2:
        conv_docs.append(objdict_to_dict(doc))
    yaml.dump_all(conv_docs, stream)


def dump(doc, stream):
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.dump(objdict_to_dict(doc), stream)

