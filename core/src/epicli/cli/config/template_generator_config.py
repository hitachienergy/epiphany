aws_templates_paths = {
    "infrastructure/virtual-machine": "static/terraform_templates_aws/vm_template.tf.j2",
    "epiphany-cluster": "static/terraform_templates_aws/epiphany_cluster.tf.j2",
    "infrastructure/vpc": "static/terraform_templates_aws/vpc.tf.j2",
    "infrastructure/internet-gateway": "static/terraform_templates_aws/internet_gateway.tf.j2",
    "infrastructure/route-table": "static/terraform_templates_aws/route_table.tf.j2",
    "infrastructure/subnet": "static/terraform_templates_aws/subnet.tf.j2",
    "infrastructure/security-group": "static/terraform_templates_aws/security_group.tf.j2",
    "infrastructure/route-table-association": "static/terraform_templates_aws/route_table_association.tf.j2",
    "infrastructure/launch-configuration": "static/terraform_templates_aws/launch_configuration.tf.j2"}

azure_templates_paths = {
    "infrastructure/virtual-machine": "static/terraform_templates_azure/vm_template.tf.j2",
    "infrastructure/network": "static/terraform_templates_azure/network_template.tf.j2",
    "epiphany-cluster": "static/terraform_templates_azure/epiphany_cluster.tf.j2",
    "infrastructure/net": "static/terraform_templates_azure/net.tf.j2"}

templates_paths = {"aws": aws_templates_paths, "azure": azure_templates_paths}
