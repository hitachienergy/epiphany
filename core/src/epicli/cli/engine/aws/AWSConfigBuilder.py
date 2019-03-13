from cli.engine.InfrastructureConfigBuilder import InfrastructureConfigBuilder
from cli.helpers.list_helpers import select_first
import cli.models.data_file_consts as model_constants
from cli.helpers.defaults_loader import load_file_from_defaults
from cli.helpers.config_merger import merge_with_defaults


class AWSConfigBuilder(InfrastructureConfigBuilder):
    def build(self, cluster_model, user_input):
        # todo generate all AWS infra docs
        result = list()
        vpc_config = self.get_vpc_config(cluster_model, user_input)
        result.append(vpc_config)
        result += self.get_autoscaling_groups_configs(cluster_model, user_input, vpc_config)
        return result

    def get_vpc_config(self, cluster_model, user_input):
        vpc_config = self.get_config_or_default(user_input, 'infrastructure/vpc')
        vpc_config["specification"]["address_pool"] = cluster_model["specification"]["cloud"]["vnet_address_pool"]
        vpc_config["specification"]["name"] = cluster_model["specification"]["cloud"]["cluster_name"].lower()+'vpc'
        return vpc_config

    def get_autoscaling_groups_configs(self, cluster_model, user_input, vpc_config):
        result = list()

        subnet_index = 0
        for component_key, component_value in cluster_model["specification"]["components"].items():
            if component_value["count"] < 1:
                continue
            subnet = select_first(result, lambda item: item[model_constants.KIND] == 'infrastructure/subnet' and item["specification"]["cidr_block"] == component_value["subnet_address_pool"])
            if subnet is None:
                subnet = self.get_config_or_default(user_input, 'infrastructure/subnet')
                subnet["specification"]["vpc_name"] = vpc_config["specification"]["name"]
                subnet["specification"]["cidr_block"] = component_value["subnet_address_pool"]
                subnet["specification"]["name"] = 'aws_subnet'+cluster_model["specification"]["cloud"]["cluster_name"].lower()+'-'+str(subnet_index)
                subnet_index += 1
                result.append(subnet)

            autoscaling_group = self.get_virtual_machine(component_value, cluster_model, user_input)
            autoscaling_group["specification"]["name"] = cluster_model["specification"]["cloud"]["cluster_name"].lower()+component_key
            autoscaling_group["specification"]["count"] = component_value["count"]
            autoscaling_group["specification"]["subnet"] = subnet["specification"]["name"]
            autoscaling_group["specification"]["tags"].append({'feature':component_key})

            result.append(autoscaling_group)

        return result

    @staticmethod
    def get_config_or_default(user_input, kind):
        config = select_first(user_input, lambda x: x[model_constants.KIND] == kind)
        if config is None:
            return load_file_from_defaults('aws', kind)

    @staticmethod
    def get_virtual_machine(component_value, cluster_model, user_input):
        machine_selector = component_value["machine"]
        model_with_defaults = select_first(user_input, lambda x: x[model_constants.KIND] == 'infrastructure/virtual-machine' and x[model_constants.NAME] == machine_selector)
        if model_with_defaults is None:
            model_with_defaults = merge_with_defaults(cluster_model[model_constants.PROVIDER], 'infrastructure/virtual-machine', machine_selector)

        return model_with_defaults
