def to_role_name(feature_name):
    return feature_name.replace("-", "_")


def to_feature_name(role_name):
    return role_name.replace("_", "-")
