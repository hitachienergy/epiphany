from cli.helpers.doc_list_helpers import select_first
from cli.helpers.data_loader import load_yaml_obj, types
from cli.helpers.config_merger import merge_with_defaults
from cli.engine.aws.APIProxy import APIProxy
from cli.helpers.Step import Step
from cli.helpers.doc_list_helpers import select_single
from cli.helpers.build_saver import get_terraform_path
from cli.helpers.data_loader import load_json_obj
import os
import uuid

class InfrastructureBuilder(Step):
    def __init__(self, docs):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.cluster_name = self.cluster_model.specification.name.lower()
        self.docs = docs

    def run(self):
        infrastructure = []

        public_key_config = self.get_public_key()
        infrastructure.append(public_key_config)

        vpc_config = self.get_vpc_config()
        infrastructure.append(vpc_config)
        vpc_name = vpc_config.specification.name

        resource_group = self.get_resource_group()
        infrastructure.append(resource_group)

        internet_gateway = self.get_internet_gateway(vpc_config.specification.name)
        infrastructure.append(internet_gateway)
        route_table = self.get_routing_table(vpc_name, internet_gateway.specification.name)
        infrastructure.append(route_table)

        subnet_index = 0

        for component_key, component_value in self.cluster_model.specification.components.items():
            if component_value['count'] < 1:
                continue
            subnet = select_first(infrastructure, lambda item: item.kind == 'infrastructure/subnet' and
                                  item.specification.cidr_block == component_value.subnet_address_pool)
            security_group = select_first(infrastructure, lambda item: item.kind == 'infrastructure/security-group' and
                                          item.specification.cidr_block == component_value.subnet_address_pool)

            if subnet is None:
                subnet = self.get_subnet(component_value, subnet_index, vpc_name)
                infrastructure.append(subnet)

                security_group = self.get_security_group(subnet, subnet_index, vpc_name)
                infrastructure.append(security_group)

                route_table_association = self.get_route_table_association(route_table.specification.name,
                                                                           subnet.specification.name, subnet_index)
                infrastructure.append(route_table_association)

                subnet_index += 1

            autoscaling_group = self.get_autoscaling_group(component_key, component_value,
                                                           subnet.specification.name)

            security_group.specification.rules += autoscaling_group.specification.security.rules

            launch_configuration = self.get_launch_configuration(autoscaling_group, component_key,
                                                                 security_group.specification.name)

            launch_configuration.specification.key_name = public_key_config.specification.key_name

            self.set_image_id_for_launch_configuration(self.cluster_model, self.docs, launch_configuration,
                                                       autoscaling_group)
            autoscaling_group.specification.launch_configuration = launch_configuration.specification.name

            infrastructure.append(autoscaling_group)
            infrastructure.append(launch_configuration)

        return infrastructure

    def get_resource_group(self):
        resource_group = self.get_config_or_default(self.docs, 'infrastructure/resource-group')
        resource_group.specification.name = self.cluster_name
        resource_group.specification.cluster_name = self.cluster_name
        return resource_group

    def get_vpc_config(self):
        vpc_config = self.get_config_or_default(self.docs, 'infrastructure/vpc')
        vpc_config.specification.address_pool = self.cluster_model.specification.cloud.vnet_address_pool
        vpc_config.specification.name = "aws-vpc-" + self.cluster_name
        vpc_config.specification.cluster_name = self.cluster_name
        return vpc_config

    def get_autoscaling_group(self, component_key, component_value, subnet_name):
        autoscaling_group = self.get_virtual_machine(component_value, self.cluster_model, self.docs)
        autoscaling_group.specification.cluster_name = self.cluster_name
        autoscaling_group.specification.name = 'aws-asg-' + self.cluster_name + '-' + component_key.lower()
        autoscaling_group.specification.count = component_value.count
        autoscaling_group.specification.subnet = subnet_name
        autoscaling_group.specification.tags.append({component_key: ''})
        autoscaling_group.specification.cluster_name = self.cluster_name
        return autoscaling_group

    def get_launch_configuration(self, autoscaling_group, component_key, security_group_name):
        launch_configuration = self.get_config_or_default(self.docs, 'infrastructure/launch-configuration')
        launch_configuration.specification.name = 'aws-launch-config-' + self.cluster_name + '-' \
                                                  + component_key.lower()
        launch_configuration.specification.size = autoscaling_group.specification.size
        launch_configuration.specification.security_groups = [security_group_name]
        return launch_configuration

    def get_subnet(self, component_value, subnet_index, vpc_name):
        subnet = self.get_config_or_default(self.docs, 'infrastructure/subnet')
        subnet.specification.vpc_name = vpc_name
        subnet.specification.cidr_block = component_value.subnet_address_pool
        subnet.specification.name = 'aws-subnet-' + self.cluster_name + '-' + str(subnet_index)
        subnet.specification.cluster_name = self.cluster_name
        return subnet

    def get_security_group(self, subnet, subnet_index, vpc_name):
        security_group = self.get_config_or_default(self.docs, 'infrastructure/security-group')
        security_group.specification.name = 'aws-security-group-' + self.cluster_name + '-' + str(subnet_index)
        security_group.specification.vpc_name = vpc_name
        security_group.specification.cidr_block = subnet.specification.cidr_block
        security_group.specification.cluster_name = self.cluster_name
        return security_group

    def get_route_table_association(self, route_table_name, subnet_name, subnet_index):
        route_table_association = self.get_config_or_default(self.docs, 'infrastructure/route-table-association')
        route_table_association.specification.name = 'aws-route-association-' + self.cluster_name + '-' + str(subnet_index)
        route_table_association.specification.subnet_name = subnet_name
        route_table_association.specification.route_table_name = route_table_name
        return route_table_association

    def get_internet_gateway(self, vpc_name):
        internet_gateway = self.get_config_or_default(self.docs, 'infrastructure/internet-gateway')
        internet_gateway.specification.name = 'aws-internet-gateway-' + self.cluster_name
        internet_gateway.specification.vpc_name = vpc_name
        internet_gateway.specification.cluster_name = self.cluster_name
        return internet_gateway

    def get_routing_table(self, vpc_name, internet_gateway_name):
        route_table = self.get_config_or_default(self.docs, 'infrastructure/route-table')
        route_table.specification.name = 'aws-route-table-' + self.cluster_name
        route_table.specification.vpc_name = vpc_name
        route_table.specification.route.gateway_name = internet_gateway_name
        route_table.specification.cluster_name = self.cluster_name
        return route_table

    def get_public_key(self):
        public_key_config = self.get_config_or_default(self.docs, 'infrastructure/public-key')
        public_key_config.specification.name = self.cluster_model.specification.admin_user.name

        # To avoid key-pair collisions on AWS we generate a randomized key to store it. In order to successfully
        # re-run TF we need to re-use the randomized key which we extract from the terraform.tfstate from the previous
        # run.
        tfstate_path = get_terraform_path(self.cluster_model.specification.name) + '/terraform.tfstate'
        if os.path.isfile(tfstate_path):
            tfstate = load_json_obj(tfstate_path)
            public_key_config.specification.key_name = \
                tfstate['modules'][0]['resources']['aws_key_pair.' + public_key_config.specification.name]['primary']['id']
        else:
            public_key_config.specification.key_name = self.cluster_model.specification.admin_user.name + '-' \
                                                       + str(uuid.uuid4())

        with open(self.cluster_model.specification.admin_user.key_path+'.pub', 'r') as stream:
            public_key_config.specification.public_key = stream.read().rstrip()

        return public_key_config

    @staticmethod
    def set_image_id_for_launch_configuration(cluster_model, docs, launch_configuration, autoscaling_group):
        with APIProxy(cluster_model, docs) as proxy:
            image_id = proxy.get_image_id(autoscaling_group.specification.os_full_name)
            launch_configuration.specification.image_id = image_id

    @staticmethod
    def get_config_or_default(docs, kind):
        config = select_first(docs, lambda x: x.kind == kind)
        if config is None:
            return load_yaml_obj(types.DEFAULT, 'aws', kind)
        return config

    @staticmethod
    def get_virtual_machine(component_value, cluster_model, docs):
        machine_selector = component_value.machine
        model_with_defaults = select_first(docs, lambda x: x.kind == 'infrastructure/virtual-machine' and
                                                                 x.name == machine_selector)
        if model_with_defaults is None:
            model_with_defaults = merge_with_defaults(cluster_model.provider, 'infrastructure/virtual-machine',
                                                      machine_selector)

        return model_with_defaults

