from cli.helpers.doc_list_helpers import select_first
from cli.helpers.data_loader import load_yaml_obj, types
from cli.helpers.config_merger import merge_with_defaults
from cli.engine.aws.APIProxy import APIProxy
from cli.helpers.Step import Step
from cli.helpers.doc_list_helpers import select_single, select_all
from cli.helpers.build_saver import get_terraform_path
from cli.helpers.data_loader import load_json_obj
from cli.helpers.naming_helpers import resource_name
import os
import uuid

class InfrastructureBuilder(Step):
    def __init__(self, docs):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.cluster_name = self.cluster_model.specification.name.lower()
        self.cluster_prefix = self.cluster_model.specification.prefix.lower()
        self.docs = docs

    def run(self):
        infrastructure = []

        public_key_config = self.get_public_key()
        infrastructure.append(public_key_config)

        vpc_config = self.get_vpc_config()

        infrastructure.append(vpc_config)
        default_security_group = self.get_default_security_group_config(vpc_config)
        infrastructure.append(default_security_group)

        vpc_name = vpc_config.specification.name

        resource_group = self.get_resource_group()
        infrastructure.append(resource_group)

        internet_gateway = self.get_internet_gateway(vpc_config.specification.name)
        infrastructure.append(internet_gateway)
        route_table = self.get_routing_table(vpc_name, internet_gateway.specification.name)
        infrastructure.append(route_table)

        efs_config = self.get_efs_config()

        for component_key, component_value in self.cluster_model.specification.components.items():
            if component_value['count'] < 1:
                continue

            subnets_to_create = []
            security_groups_to_create = []
            subnet_index = 0
            for subnet_definition in component_value.subnets:  # todo extract to another method or class
                subnet = select_first(infrastructure, lambda item: item.kind == 'infrastructure/subnet' and
                                      item.specification.cidr_block == subnet_definition['address_pool'])
                security_group = select_first(infrastructure, lambda item: item.kind == 'infrastructure/security-group' and
                                              item.specification.cidr_block == subnet_definition['address_pool'])

                if subnet is None:
                    subnet = self.get_subnet(subnet_definition, component_key, vpc_name, subnet_index)
                    infrastructure.append(subnet)

                    security_group = self.get_security_group(subnet, component_key, vpc_name, subnet_index)
                    infrastructure.append(security_group)

                    route_table_association = self.get_route_table_association(route_table.specification.name,
                                                                               component_key,
                                                                               subnet.specification.name, subnet_index)
                    infrastructure.append(route_table_association)
                    subnet_index += 1

                subnets_to_create.append(subnet)
                security_groups_to_create.append(security_group)

            autoscaling_group = self.get_autoscaling_group(component_key, component_value, subnets_to_create)

            for security_group in security_groups_to_create:
                security_group.specification.rules += autoscaling_group.specification.security.rules

            launch_configuration = self.get_launch_configuration(autoscaling_group, component_key,
                                                                 security_groups_to_create)

            launch_configuration.specification.key_name = public_key_config.specification.key_name

            self.set_image_id_for_launch_configuration(self.cluster_model, self.docs, launch_configuration,
                                                       autoscaling_group)
            autoscaling_group.specification.launch_configuration = launch_configuration.specification.name

            if autoscaling_group.specification.mount_efs:
                for subnet in subnets_to_create:
                    self.efs_add_mount_target_config(efs_config, subnet)

            infrastructure.append(autoscaling_group)
            infrastructure.append(launch_configuration)

        if self.has_efs_any_mounts(efs_config):
            infrastructure.append(efs_config)
            self.add_security_rules_inbound_efs(infrastructure, default_security_group)

        return infrastructure

    def get_resource_group(self):
        resource_group = self.get_config_or_default(self.docs, 'infrastructure/resource-group')
        resource_group.specification.name = self.cluster_name
        resource_group.specification.cluster_name = self.cluster_name
        return resource_group

    def get_vpc_config(self):
        vpc_config = self.get_config_or_default(self.docs, 'infrastructure/vpc')
        vpc_config.specification.address_pool = self.cluster_model.specification.cloud.vnet_address_pool
        vpc_config.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'vpc')
        vpc_config.specification.cluster_name = self.cluster_name
        return vpc_config

    def get_default_security_group_config(self, vpc_config):
        sg_config = self.get_config_or_default(self.docs, 'infrastructure/default-security-group')
        sg_config.specification.vpc_name = vpc_config.specification.name
        return sg_config

    def get_efs_config(self):
        efs_config = self.get_config_or_default(self.docs, 'infrastructure/efs-storage')
        efs_config.specification.token = "aws-efs-token-" + self.cluster_name
        efs_config.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'efs')
        return efs_config

    def get_autoscaling_group(self, component_key, component_value, subnets_to_create):
        autoscaling_group = self.get_virtual_machine(component_value, self.cluster_model, self.docs)
        autoscaling_group.specification.cluster_name = self.cluster_name
        autoscaling_group.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'asg', component_key)
        autoscaling_group.specification.count = component_value.count
        autoscaling_group.specification.subnet_names = [s.specification.name for s in subnets_to_create]
        autoscaling_group.specification.availability_zones = list(set([s.specification.availability_zone for s in subnets_to_create]))
        autoscaling_group.specification.tags.append({'cluster_name': self.cluster_name})
        autoscaling_group.specification.tags.append({component_key: ''})
        return autoscaling_group

    def get_launch_configuration(self, autoscaling_group, component_key, security_groups_to_create):
        launch_configuration = self.get_config_or_default(self.docs, 'infrastructure/launch-configuration')
        launch_configuration.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'launch-config', component_key)
        launch_configuration.specification.size = autoscaling_group.specification.size
        launch_configuration.specification.security_groups = [s.specification.name for s in security_groups_to_create]
        launch_configuration.specification.disks = autoscaling_group.specification.disks
        launch_configuration.specification.ebs_optimized = autoscaling_group.specification.ebs_optimized
        launch_configuration.specification.associate_public_ip = self.cluster_model.specification.cloud.use_public_ips
        return launch_configuration

    def get_subnet(self, subnet_definition, component_key, vpc_name, index):
        subnet = self.get_config_or_default(self.docs, 'infrastructure/subnet')
        subnet.specification.vpc_name = vpc_name
        subnet.specification.cidr_block = subnet_definition['address_pool']
        subnet.specification.availability_zone = subnet_definition['availability_zone']
        subnet.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'subnet' + '-' + str(index), component_key)
        subnet.specification.cluster_name = self.cluster_name
        return subnet

    def get_security_group(self, subnet, component_key, vpc_name, index):
        security_group = self.get_config_or_default(self.docs, 'infrastructure/security-group')
        security_group.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'security-group' + '-' + str(index), component_key)
        security_group.specification.vpc_name = vpc_name
        security_group.specification.cidr_block = subnet.specification.cidr_block
        security_group.specification.cluster_name = self.cluster_name
        return security_group

    def get_route_table_association(self, route_table_name, component_key, subnet_name, subnet_index):
        route_table_association = self.get_config_or_default(self.docs, 'infrastructure/route-table-association')
        route_table_association.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'route-association', component_key + '-' + str(subnet_index))
        route_table_association.specification.subnet_name = subnet_name
        route_table_association.specification.route_table_name = route_table_name
        return route_table_association

    def get_internet_gateway(self, vpc_name):
        internet_gateway = self.get_config_or_default(self.docs, 'infrastructure/internet-gateway')
        internet_gateway.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'internet-gateway')
        internet_gateway.specification.vpc_name = vpc_name
        internet_gateway.specification.cluster_name = self.cluster_name
        return internet_gateway

    def get_routing_table(self, vpc_name, internet_gateway_name):
        route_table = self.get_config_or_default(self.docs, 'infrastructure/route-table')
        route_table.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'route-table')
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
        if os.path.isfile(self.cluster_model.specification.admin_user.key_path + '.pub'):
            with open(self.cluster_model.specification.admin_user.key_path + '.pub', 'r') as stream:
                public_key_config.specification.public_key = stream.read().rstrip()
        else:
            self.logger.error(
                'SSH key path "' + self.cluster_model.specification.admin_user.key_path + '.pub' +
                '" is not valid. Ansible run will fail.')

        return public_key_config

    def add_security_rules_inbound_efs(self, infrastructure, security_group):
        ags_allowed_to_efs = select_all(infrastructure, lambda item: item.kind == 'infrastructure/virtual-machine' and
                                                      item.specification.authorized_to_efs)

        for asg in ags_allowed_to_efs:
            for subnet_in_asg in asg.specification.subnet_names:
                subnet = select_single(infrastructure, lambda item: item.kind == 'infrastructure/subnet' and
                                                                   item.specification.name == subnet_in_asg)

                rule_defined = select_first(security_group.specification.rules, lambda item: item.source_address_prefix == subnet.specification.cidr_block
                                                                                            and item.destination_port_range == 2049)
                if rule_defined is None:
                    rule = self.get_config_or_default(self.docs, 'infrastructure/security-group-rule')
                    rule.specification.name = 'sg-rule-nfs-default-from-'+subnet.specification.name
                    rule.specification.direction = 'ingress'
                    rule.specification.protocol = 'tcp'
                    rule.specification.description = 'NFS inbound for '+subnet.specification.name
                    rule.specification.access = 'Allow'

                    rule.specification.source_port_range = -1
                    rule.specification.destination_port_range = 2049

                    rule.specification.source_address_prefix = subnet.specification.cidr_block
                    rule.specification.destination_address_prefix = '*'
                    security_group.specification.rules.append(rule.specification)

    @staticmethod
    def efs_add_mount_target_config(efs_config, subnet):
        target = select_first(efs_config.specification.mount_targets,
                              lambda item: item['availability_zone'] == subnet.specification.availability_zone)
        if target is None:
            efs_config.specification.mount_targets.append(
                {'name': 'efs-'+subnet.specification.name+'-mount',
                 'subnet_name': subnet.specification.name,
                 'availability_zone': subnet.specification.availability_zone})

    @staticmethod
    def has_efs_any_mounts(efs_config):
        if len(efs_config.specification.mount_targets) > 0:
            return True
        return False

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
