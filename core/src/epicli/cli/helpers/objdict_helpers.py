from copy import deepcopy
from collections.abc import Iterable

from cli.helpers.ObjDict import ObjDict
from cli.helpers.doc_list_helpers import select_all


class DuplicatesInNamedListException(Exception):
    pass


class TypeMismatchException(Exception):
    pass


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
    return isinstance(l, Iterable) and all(hasattr(x, 'name') for x in l)


def assert_unique_names_in_named_list(list, key, type): 
    all_names = [x["name"] for x in list] 
    for name in all_names: 
        if all_names.count(name) > 1: 
            raise DuplicatesInNamedListException( f'"name" field with value "{name}" occurs multiple times in list "{key}" in {type} definition.' )


# to_merge is passed by reference, item under key is updated, extended or replaced 
def merge_list(to_merge, extend_by, key):
    if is_named_list(to_merge[key]) and is_named_list(extend_by):
        # ensure all items have unique names in to_merge and extend_by
        assert_unique_names_in_named_list(to_merge[key], key, 'default')    
        assert_unique_names_in_named_list(extend_by, key, 'input')

        # Merge possible matched objects from extend_by to to_merge
        for m_i in to_merge[key]:   
            count = select_all(extend_by, lambda x: x['name'] == m_i['name'])
            if len(count) == 1:
                merge_objdict(m_i, count[0])

        # Add non-matched objects from extend_by to to_merge. Might be extra config used by projects.
        for e_i in extend_by:   
            count = select_all(to_merge[key], lambda x: x['name'] == e_i['name'])
            if len(count) == 0:
                to_merge[key].append(e_i)
    else:
        # No named list so just replace item
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
                # Dealing with 2 basic types (integer, boolean, string, etc.) so replace
                to_merge[key] = val
            else:
                # If we come here we are dealing with 2 different types we cannot merge so throw exception.
                raise TypeMismatchException(f'Types of key "{key}" are different: {type(to_merge[key])}, {type(val)}. Unable to merge.')
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
