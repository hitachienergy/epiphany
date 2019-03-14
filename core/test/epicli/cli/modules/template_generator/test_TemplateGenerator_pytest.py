import pytest
import yaml

from core.src.epicli.cli.modules.template_generator import TemplateGenerator

DOCUMENT_NO_PROVIDER = \
    """kind: infrastructure/virtual-machine
version: 0.3.0
title: "Virtual Machine Infra"
name: my-test-master-aws
specification:
 size: Standard_DS2_v2"""

DOCUMENT_NO_VALUE_FROM_TEMPLATE = \
    """kind: infrastructure/virtual-machine
version: 0.3.0
title: "Virtual Machine Infra"
provider: aws
specification:
 size: Standard_DS2_v2"""

DOCUMENT_PROPER_NOT_EXISTING_TEMPLATE = \
    """kind: infrastructure/not-existing-template
version: 0.3.0
title: "Virtual Machine Infra"
provider: aws
name: my-test-master-az
specification:
 size: Standard_DS2_v2"""

DOCUMENT_PROPER_VM_AZURE = \
    """kind: infrastructure/virtual-machine
version: 0.3.0
title: "Virtual Machine Infra"
provider: azure
name: my-test-master-az
specification:
 size: Standard_DS2_v2"""

DOCUMENT_PROPER_NETWORK_AZURE = \
    """kind: infrastructure/network
name: my-test-net-az
provider: azure
specification:
 some_setting: setting2
title: Network Config
version: 0.3.0
"""

RESULT_PROPER_TERRAFORM_CONTENT_VM_AZURE = \
    """#####################################################
# VMs - my-test-master-az
#####################################################"""

RESULT_PROPER_TERRAFORM_CONTENT_NETWORK_AZURE = \
    """#####################################################
# Network - my-test-net-az
#####################################################"""

DOCUMENT_PROPER_VM_AWS = \
    """kind: infrastructure/virtual-machine
version: 0.3.0
title: "Virtual Machine Infra"
provider: aws
name: my-test-master-aws
specification:
 size: Standard_DS2_v2"""

DOCUMENT_PROPER_NETWORK_AWS = \
    """kind: infrastructure/network
name: my-test-net-aws
provider: aws
specification:
 some_setting: setting2
title: Network Config
version: 0.3.0
"""

RESULT_PROPER_TERRAFORM_CONTENT_VM_AWS = \
    """#####################################################
# VMs - my-test-master-aws
#####################################################"""

RESULT_PROPER_TERRAFORM_CONTENT_NETWORK_AWS = \
    """#####################################################
# Network - my-test-net-aws
#####################################################"""

aws_templates_paths = {"infrastructure/virtual-machine": "static/tests/terraform_templates_aws/vm_template.tf.j2",
                       "infrastructure/network": "static/tests/terraform_templates_aws/network_template.tf.j2",
                       "infrastructure/not-existing-template": "static/tests/not-existing-template.tf.j2"}

azure_templates_paths = {
    "infrastructure/virtual-machine": "static/tests/terraform_templates_azure/vm_template.tf.j2",
    "infrastructure/network": "static/tests/terraform_templates_azure/network_template.tf.j2"}

templates_paths = {"aws": aws_templates_paths, "azure": azure_templates_paths}


def test_should_generate_proper_terraform_content_vm_aws():
    # given:
    template_generator = TemplateGenerator.TemplateGenerator()
    document = yaml.load(DOCUMENT_PROPER_VM_AWS)

    # when:
    content = template_generator.generate_terraform_file_content(document=document, templates_paths=templates_paths)

    # then:
    assert RESULT_PROPER_TERRAFORM_CONTENT_VM_AWS == content


def test_should_generate_proper_terraform_content_network_aws():
    # given:
    template_generator = TemplateGenerator.TemplateGenerator()
    document = yaml.load(DOCUMENT_PROPER_NETWORK_AWS)

    # when:
    content = template_generator.generate_terraform_file_content(document=document, templates_paths=templates_paths)

    # then:
    assert RESULT_PROPER_TERRAFORM_CONTENT_NETWORK_AWS == content


def test_should_generate_proper_terraform_content_vm_azure():
    # given:
    template_generator = TemplateGenerator.TemplateGenerator()
    document = yaml.load(DOCUMENT_PROPER_VM_AZURE)

    # when:
    content = template_generator.generate_terraform_file_content(document=document, templates_paths=templates_paths)

    # then:
    assert RESULT_PROPER_TERRAFORM_CONTENT_VM_AZURE == content


def test_should_generate_proper_terraform_content_network_azure():
    # given:
    template_generator = TemplateGenerator.TemplateGenerator()
    document = yaml.load(DOCUMENT_PROPER_NETWORK_AZURE)

    # when:
    content = template_generator.generate_terraform_file_content(document=document, templates_paths=templates_paths)

    # then:
    assert RESULT_PROPER_TERRAFORM_CONTENT_NETWORK_AZURE == content


def test_should_fail_on_no_provider():
    # given:
    template_generator = TemplateGenerator.TemplateGenerator()
    document = yaml.load(DOCUMENT_NO_PROVIDER)

    # when:
    # then:
    with pytest.raises(Exception):
        template_generator.generate_terraform_file_content(document=document, templates_paths=templates_paths)


def test_should_fail_on_no_name():
    # given:
    template_generator = TemplateGenerator.TemplateGenerator()
    document = yaml.load(DOCUMENT_NO_VALUE_FROM_TEMPLATE)

    # when:
    with pytest.raises(SystemExit) as e:
        template_generator.generate_terraform_file_content(document=document, templates_paths=templates_paths)

    # then:
    assert e.type == SystemExit
    assert e.value.code == 1


def test_should_fail_on_not_existing_template():
    # given:
    template_generator = TemplateGenerator.TemplateGenerator()
    document = yaml.load(DOCUMENT_PROPER_NOT_EXISTING_TEMPLATE)

    # when:
    with pytest.raises(SystemExit) as e:
        template_generator.generate_terraform_file_content(document=document, templates_paths=templates_paths)

    # then:
    assert e.type == SystemExit
    assert e.value.code == 1
