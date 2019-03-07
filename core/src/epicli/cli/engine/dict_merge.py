
def merge_dict(to_merge, extend_by):
    for key, val in extend_by.items():
        if key in to_merge:
            if isinstance(to_merge[key], dict):  # if element is an object - merge it
                merge_dict(to_merge[key], val)
            else:
                to_merge[key] = val
        else:
            to_merge[key] = val
