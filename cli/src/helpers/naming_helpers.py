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


def get_os_name_normalized(vm_doc):
    expected_indicators = {
        "ubuntu": "ubuntu",
    }
    if vm_doc.provider == "azure":
        # Example image offers:
        # - 0001-com-ubuntu-server-focal
        for indicator in expected_indicators:
            if indicator in vm_doc.specification.storage_image_reference.offer.lower():
                return expected_indicators[indicator]
    if vm_doc.provider == "aws":
        # Example public/official AMI names:
        # - ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20221010
        for indicator in expected_indicators:
            if indicator in vm_doc.specification.os_full_name.lower():
                return expected_indicators[indicator]
    # When name is completely custom
    return None
