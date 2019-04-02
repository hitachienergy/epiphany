from cli.helpers.doc_list_helpers import select_first
from cli.helpers.data_loader import load_data_file
from cli.helpers.config_merger import merge_with_defaults
from cli.engine.aws.APIProxy import APIProxy
import cli.helpers.data_types as data_types
from helpers.Step import Step


class InfrastructureBuilder(Step):
    def __init__(self):
        super().__init__(__name__)

    def run(self, cluster_model, user_input):
        result = []
        vpc_config = self.get_vpc_config(cluster_model, user_input)
        result.append(vpc_config)
        vpc_name = vpc_config.specification.name
        cluster_name = cluster_model.specification.name.lower()

        internet_gateway = self.get_internet_gateway(cluster_name, user_input, vpc_config.specification.name)
        result.append(internet_gateway)
        route_table = self.get_routing_table(cluster_name, user_input, vpc_name, internet_gateway.specification.name)
        result.append(route_table)

        subnet_index = 0
        for component_key, component_value in cluster_model.specification.components.items():
            if component_value['count'] < 1:
                continue
            subnet = select_first(result, lambda item: item.kind == 'infrastructure/subnet' and item.specification.cidr_block == component_value.subnet_address_pool)
            security_group = select_first(result, lambda item: item.kind == 'infrastructure/security-group' and item.specification.cidr_block == component_value.subnet_address_pool)

            if subnet is None:
                subnet = self.get_subnet(cluster_name, component_value, subnet_index, user_input, vpc_name)
                result.append(subnet)

                security_group = self.get_security_group(cluster_name, subnet, subnet_index, user_input, vpc_name)
                result.append(security_group)

                route_table_association = self.get_route_table_association(cluster_name, user_input, route_table.specification.name, subnet.specification.name, subnet_index)
                result.append(route_table_association)

                subnet_index += 1

            autoscaling_group = self.get_autoscaling_group(cluster_model, component_key, component_value, subnet.specification.name, user_input)

            security_group.specification.rules += autoscaling_group.specification.security.rules

            launch_configuration = self.get_launch_configuration(autoscaling_group, cluster_name, component_key, security_group.specification.name, user_input)

            self.set_image_id_for_launch_configuration(cluster_model, user_input, launch_configuration, autoscaling_group)
            autoscaling_group.specification.launch_configuration = launch_configuration.specification.name

            result.append(autoscaling_group)
            result.append(launch_configuration)

        return result

    def get_vpc_config(self, cluster_model, user_input):
        vpc_config = self.get_config_or_default(user_input, 'infrastructure/vpc')
        vpc_config.specification.address_pool = cluster_model.specification.cloud.vnet_address_pool
        vpc_config.specification.name = "aws-vpc-" + cluster_model.specification.name.lower()
        return vpc_config

    def get_autoscaling_group(self, cluster_model, component_key, component_value, subnet_name, user_input):
        cluster_name = cluster_model.specification.name.lower()
        autoscaling_group = self.get_virtual_machine(component_value, cluster_model, user_input)
        autoscaling_group.specification.name = 'aws-asg-' + cluster_name + '-' + component_key.lower()
        autoscaling_group.specification.count = component_value.count
        autoscaling_group.specification.subnet = subnet_name
        autoscaling_group.specification.tags.append({component_key: ''})
        autoscaling_group.specification.tags.append({'cluster_name': cluster_name})
        return autoscaling_group

    def get_launch_configuration(self, autoscaling_group, cluster_name, component_key, security_group_name, user_input):
        launch_configuration = self.get_config_or_default(user_input, 'infrastructure/launch-configuration')
        launch_configuration.specification.name = 'aws-launch-config-' + cluster_name.lower() + '-' + component_key.lower()
        launch_configuration.specification.size = autoscaling_group.specification.size
        launch_configuration.specification.security_groups = [security_group_name]
        return launch_configuration

    def get_subnet(self, cluster_name, component_value, subnet_index, user_input, vpc_name):
        subnet = self.get_config_or_default(user_input, 'infrastructure/subnet')
        subnet.specification.vpc_name = vpc_name
        subnet.specification.cidr_block = component_value.subnet_address_pool
        subnet.specification.name = 'aws-subnet-' + cluster_name + '-' + str(subnet_index)
        return subnet

    def get_security_group(self, cluster_name, subnet, subnet_index, user_input, vpc_name):
        security_group = self.get_config_or_default(user_input, 'infrastructure/security-group')
        security_group.specification.name = 'aws-security-group-' + cluster_name + '-' + str(subnet_index)
        security_group.specification.vpc_name = vpc_name
        security_group.specification.cidr_block = subnet.specification.cidr_block
        return security_group

    def get_route_table_association(self, cluster_name, user_input, route_table_name, subnet_name, subnet_index):
        route_table_association = self.get_config_or_default(user_input, 'infrastructure/route-table-association')
        route_table_association.specification.name = 'aws-route-association-' + cluster_name + '-' + str(subnet_index)
        route_table_association.specification.subnet_name = subnet_name
        route_table_association.specification.route_table_name = route_table_name
        return route_table_association

    def get_internet_gateway(self, cluster_name, user_input, vpc_name):
        internet_gateway = self.get_config_or_default(user_input, 'infrastructure/internet-gateway')
        internet_gateway.specification.name = 'aws-internet-gateway-' + cluster_name
        internet_gateway.specification.vpc_name = vpc_name
        return internet_gateway

    def get_routing_table(self, cluster_name, user_input, vpc_name, internet_gateway_name):
        route_table = self.get_config_or_default(user_input, 'infrastructure/route-table')
        route_table.specification.name = 'aws-route-table-' + cluster_name
        route_table.specification.vpc_name = vpc_name
        route_table.specification.route.gateway_name = internet_gateway_name
        return route_table

    @staticmethod
    def set_image_id_for_launch_configuration(cluster_model, config_docs, launch_configuration, autoscaling_group):
        with APIProxy(cluster_model, config_docs) as proxy:
            image_id = proxy.get_image_id(autoscaling_group.specification.os_full_name)
            launch_configuration.specification.image_id = image_id

    @staticmethod
    def get_config_or_default(user_input, kind):
        config = select_first(user_input, lambda x: x.kind == kind)
        if config is None:
            return load_data_file(data_types.DEFAULT, 'aws', kind)
        return config

    @staticmethod
    def get_virtual_machine(component_value, cluster_model, user_input):
        machine_selector = component_value.machine
        model_with_defaults = select_first(user_input, lambda x: x.kind == 'infrastructure/virtual-machine' and x.name == machine_selector)
        if model_with_defaults is None:
            model_with_defaults = merge_with_defaults(cluster_model.provider, 'infrastructure/virtual-machine', machine_selector)

        return model_with_defaults

