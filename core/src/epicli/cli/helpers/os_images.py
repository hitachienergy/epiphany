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
        # - ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-20210323
        # - RHEL-7.8_HVM_GA-20200225-x86_64-1-Hourly2-GP2
        # - CentOS 7.8.2003 x86_64
        for indicator in expected_indicators:
            if indicator in vm_doc.specification.os_full_name.lower():
                return expected_indicators[indicator]
    # When name is completely custom
    return None
