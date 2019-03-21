from cli.helpers.ObjDict import ObjDict


def nested_dict_to_objdict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            nested_dict_to_objdict(v)
            d[k] = ObjDict(v)

def dict_to_objdict(d):
    nested_dict_to_objdict(d)
    return ObjDict(d)


def nested_objdict_to_dict(d):
    for k, v in d.items():
        if isinstance(v, ObjDict):
            nested_objdict_to_dict(v)
            d[k] = dict(v)


def objdict_to_dict(d):
    nested_objdict_to_dict(d)
    return dict(d)


def merge_objdict(to_merge, extend_by):
    for key, val in extend_by.items():
        if key in to_merge:
            if isinstance(to_merge[key], ObjDict):  # if element is an object - merge it
                merge_objdict(to_merge[key], val)
            else:
                to_merge[key] = val
        else:
            to_merge[key] = val
