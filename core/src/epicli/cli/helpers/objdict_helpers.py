from cli.helpers.ObjDict import ObjDict
from cli.helpers.doc_list_helpers import select_all
from copy import deepcopy


def _nested_dict_to_dict(something, *, src_class, dst_class):
    if isinstance(something, src_class):
        return dst_class(
            (key, _nested_dict_to_dict(value, src_class=src_class, dst_class=dst_class))
            for key, value in something.items()
        )
    if isinstance(something, list):
        return list(
            _nested_dict_to_dict(value, src_class=src_class, dst_class=dst_class)
            for value in something
        )
    # Clone everything unexpected
    return deepcopy(something)


def dict_to_objdict(something):
    """Recursively convert any dictionary (subclass of dict) to ObjDict."""
    return _nested_dict_to_dict(something, src_class=dict, dst_class=ObjDict)


def objdict_to_dict(something):
    """Recursively convert any ObjDict to python dictionary."""
    return _nested_dict_to_dict(something, src_class=dict, dst_class=dict)  # ObjDict is a subclass of dict


def is_named_list(l):
    count = select_all(l, lambda x: hasattr(x, 'name'))
    return len(count) == len(l)


def check_duplicate_in_named_list(l, key, value, type):
        count = select_all(l, lambda x: x['name'] == value)
        if len(count) > 1:
            raise Exception(f'`name` field with value `"{value}"` occurs multiple times in list `"{key}"` in {type} definition.')


def merge_objdict(to_merge, extend_by):
    for key, val in extend_by.items():
        if key in to_merge:
            if isinstance(to_merge[key], ObjDict):
                merge_objdict(to_merge[key], val)
            elif isinstance(to_merge[key], list):
                if is_named_list(to_merge[key]) and is_named_list(val):
                    for m_i in to_merge[key]:
                        name_default = m_i['name']
                        check_duplicate_in_named_list(to_merge[key], key, name_default, 'default')     
                        for e_i in val:
                            name_extend = e_i['name']
                            check_duplicate_in_named_list(val, key, name_extend, 'input')
                            if name_default == name_extend:
                                merge_objdict(m_i, e_i)
                            #else:
                            #    count = select_all(to_merge[key], lambda x: x['name'] == name_extend)
                            #    if len(count) == 0:
                            #        to_merge[key].append(e_i)
                else:
                    to_merge[key] = val
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


def replace_yesno_with_booleans(d):
    if isinstance(d, list):
        for dd in d:
            replace_yesno_with_booleans(dd)
    elif isinstance(d, ObjDict):
        for key, val in d.items():
            if isinstance(d[key], str):
                if val == 'yes':        
                    d[key] = True
                elif val == 'no':             
                    d[key] = False
            else:      
                replace_yesno_with_booleans(d[key])
