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
        return cluster_name
    else:
        return '%s-%s' % (prefix.lower(), cluster_name.lower()) 

def storage_account_name(cluster_name, storage_use):
    pre = ''
    if len(cluster_name) > 5:
        pre = cluster_name[:5]
    else:
        pre = cluster_name

    post = ''
    if len(storage_use) > 5:
        post = storage_use[:5]
    else:
        post = storage_use        

    return pre + ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(24-len(pre)-len(post))) + post
    
    
