def get_os_distro_normalized(vm_doc):
    expected_indicators = {
        "ubuntu": "ubuntu",
        "rhel": "rhel",
        "redhat": "rhel",
        "centos": "centos",
    }
    if vm_doc.provider == "azure":
        # Example image offers:
        # - UbuntuServer
        # - RHEL
        # - CentOS
        for indicator in expected_indicators:
            if indicator in vm_doc.specification.storage_image_reference.offer.lower():
                return expected_indicators[indicator]
    if vm_doc.provider == "aws":
        # Example public/official AMI names:
        # - ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-20210907
        # - RHEL-7.9_HVM-20210208-x86_64-0-Hourly2-GP2
        # - CentOS 7.9.2009 x86_64
        for indicator in expected_indicators:
            if indicator in vm_doc.specification.os_full_name.lower():
                return expected_indicators[indicator]
    # When name is completely custom
    return None
