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


#Note: We pas to_merge by reference using key to update/extend entries.
def merge_list(to_merge, extend_by, key):
        if is_named_list(to_merge[key]) and is_named_list(extend_by):
            # Merge lists as named lists
            for m_i in to_merge[key]:
                check_duplicate_in_named_list(to_merge[key], key, m_i['name'], 'default')     
                for e_i in extend_by:
                    check_duplicate_in_named_list(extend_by, key, e_i['name'], 'input')
                    if m_i['name'] == e_i['name']:
                        merge_objdict(m_i, e_i)
                    else:
                        count = select_all(to_merge[key], lambda x: x['name'] == e_i['name'])
                        if len(count) == 0:
                            to_merge[key].append(e_i)
        else:
            # No named list so just overwrite lists from with the source
            to_merge[key] = extend_by


def merge_objdict(to_merge, extend_by):
    for key, val in extend_by.items():
        if key in to_merge:
            if isinstance(to_merge[key], ObjDict) and isinstance(val, ObjDict):
                # Dealing with 2 ObjDicts so recursively merge
                merge_objdict(to_merge[key], val)
            elif isinstance(to_merge[key], list) and isinstance(val, list):
                # Dealing with 2 lists
                merge_list(to_merge, val, key)
            elif type(to_merge[key]) == type(val):
                # Dealing with 2 base fields (integer, boolean, string ..etc) so overwrite from source to defaults
                to_merge[key] = val
            else:
                # If we come here we are dealing with 2 different types we cannot merge so throw exception.
                raise Exception(f'Types of key `"{key}"` are different: {type(to_merge[key])}, {type(val)}. Unable to merge.')
        else:
            # Field not known in defaults so just add it. Might be extra config used by projects.
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
