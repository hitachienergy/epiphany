import random
import string

def to_role_name(feature_name):
    return feature_name.replace("-", "_")


def to_feature_name(role_name):
    return role_name.replace("_", "-")


def resource_name(prefix, cluster_name, resource_type, component=None):
    name = ''
    if (not prefix) or (prefix == 'default'):
        if component is None:
            name = '%s-%s' % (cluster_name.lower(), resource_type.lower())
        else:
            name = '%s-%s-%s' % (cluster_name.lower(), component.lower(), resource_type.lower())
    else:
        if component is None:
            name = '%s-%s-%s' % (prefix.lower(), cluster_name.lower(), resource_type.lower())
        else:
            name = '%s-%s-%s-%s' % (prefix.lower(), cluster_name.lower(), component.lower(), resource_type.lower())
    return to_feature_name(name)


def cluster_tag(prefix, cluster_name):
    if (not prefix) or (prefix == 'default'):
        return cluster_name.lower()
    else:
        return '%s-%s' % (prefix.lower(), cluster_name.lower()) 


def storage_account_name(prefix, cluster_name, storage_use):
    pre = ''
    if not ((not prefix) or (prefix == 'default')):
        if len(prefix) > 8:
            pre = prefix[:8].lower()
        else:
            pre = prefix.lower() 

    sto = ''
    if len(storage_use) > 5:
        sto = storage_use[:5].lower()
    else:
        sto = storage_use.lower()    

    clu = ''
    length = 24 - (len(pre)+len(sto))
    if len(cluster_name) > length:
        clu = cluster_name[:length].lower()
    else:
        clu = cluster_name.lower()

    return f'{pre}{clu}{sto}'
    
