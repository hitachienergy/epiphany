def to_role_name(feature_name):
    return feature_name.replace("-", "_")


def to_feature_name(role_name):
    return role_name.replace("_", "-")


def resource_name(prefix, cluster_name, resource_type, component=None):
    if prefix == 'default':
        if component is None:
            return '%s-%s' % (cluster_name.lower(), resource_type.lower())
        else:
            return '%s-%s-%s' % (cluster_name.lower(), component.lower(), resource_type.lower())
    else:
        if component is None:
            return '%s-%s-%s' % (prefix.lower(), cluster_name.lower(), resource_type.lower())
        else:
            return '%s-%s-%s-%s' % (prefix.lower(), cluster_name.lower(), component.lower(), resource_type.lower())
