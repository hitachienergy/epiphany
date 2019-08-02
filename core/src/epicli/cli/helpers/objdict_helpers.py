from cli.helpers.ObjDict import ObjDict
from copy import deepcopy


def nested_dict_to_objdict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            nested_dict_to_objdict(v)
            d[k] = ObjDict(v)


def dict_to_objdict(d):
    dc = deepcopy(d)
    nested_dict_to_objdict(dc)
    return ObjDict(dc)


def nested_objdict_to_dict(d):
    for k, v in d.items():
        if isinstance(v, ObjDict):
            nested_objdict_to_dict(v)
            d[k] = dict(v)


def objdict_to_dict(d):
    dc = deepcopy(d)
    nested_objdict_to_dict(dc)
    return dict(dc)


def merge_objdict(to_merge, extend_by):
    for key, val in extend_by.items():
        if key in to_merge:
            if isinstance(to_merge[key], ObjDict):
                merge_objdict(to_merge[key], val)
            else:
                to_merge[key] = val
        else:
            to_merge[key] = val
