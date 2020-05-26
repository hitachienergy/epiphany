from cli.helpers.ObjDict import ObjDict
from copy import deepcopy


def _nested_dict_to_dict(d, *, src_class, dst_class):
    if isinstance(d, src_class):
        return dst_class(
            (k, _nested_dict_to_dict(v, src_class=src_class, dst_class=dst_class))
            for k, v in d.items()
        )
    if isinstance(d, list):
        return list(
            _nested_dict_to_dict(v, src_class=src_class, dst_class=dst_class)
            for v in d
        )
    # Clone everything unexpected
    return deepcopy(d)


def dict_to_objdict(d):
    """Recursively convert any dictionary (subclass of dict) to ObjDict."""
    return _nested_dict_to_dict(d, src_class=dict, dst_class=ObjDict)


def objdict_to_dict(d):
    """Recursively convert any ObjDict to python dictionary."""
    return _nested_dict_to_dict(d, src_class=dict, dst_class=dict)  # ObjDict is a subclass of dict


def merge_objdict(to_merge, extend_by):
    for key, val in extend_by.items():
        if key in to_merge:
            if isinstance(to_merge[key], ObjDict):
                merge_objdict(to_merge[key], val)
            else:
                to_merge[key] = val
        else:
            to_merge[key] = val


def remove_value(d, value):
    if isinstance(d, str):
        return
    elif isinstance(d, list):
        for dd in d:
            remove_value(dd, value)
    else:
        for k in list(d):
            v = d[k]
            if isinstance(v, list) or isinstance(v, dict):
                remove_value(v, value)
            else:
                if value == v:
                    del d[k]
