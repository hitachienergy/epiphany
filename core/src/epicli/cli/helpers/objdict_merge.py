from cli.helpers.ObjDict import ObjDict

def merge_objdict(to_merge, extend_by):
    for key, val in extend_by.items():
        if key in to_merge:
            if isinstance(to_merge[key], ObjDict):  # if element is an object - merge it
                merge_objdict(to_merge[key], val)
            else:
                to_merge[key] = val
        else:
            to_merge[key] = val
