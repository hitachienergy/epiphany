import os
import uuid
from copy import deepcopy

from cli.src.helpers.build_io import get_terraform_path
from cli.src.helpers.config_merger import merge_with_defaults
from cli.src.helpers.data_loader import (load_json_obj, load_schema_obj,
                                         schema_types)
from cli.src.helpers.doc_list_helpers import (select_all, select_first,
                                              select_single)
from cli.src.helpers.naming_helpers import resource_name
from cli.src.helpers.objdict_helpers import dict_to_objdict, objdict_to_dict
from cli.src.providers.aws.APIProxy import APIProxy
from cli.src.Step import Step
from cli.version import VERSION


class InfrastructureBuilder(Step):
    def __init__(self, docs, manifest_docs=[]):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.cluster_name = self.cluster_model.specification.name.lower()
        self.cluster_prefix = self.cluster_model.specification.prefix.lower()
        self.use_network_security_groups = self.cluster_model.specification.cloud.network.use_network_security_groups
        self.use_public_ips = self.cluster_model.specification.cloud.use_public_ips
        self.docs = docs
        self.manifest_docs = manifest_docs

        # If there are no security groups Ansible provisioning will fail because
        # SSH is not allowed then with public IPs on AWS.
        if not(self.use_network_security_groups) and self.use_public_ips:
            self.logger.warning('Use of security groups has been disabled and public IPs are used. Ansible run will fail because SSH will not be allowed.')

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
            vm_count = component_value['count']
            if vm_count < 1:
                continue

            # The vm config also contains some other stuff we use for network and security config.
            # So get it here and pass it allong.
            vm_config = self.get_virtual_machine(component_value)

            # For now only one subnet per component.
            if (len(component_value.subnets) > 1):
                self.logger.warning('On AWS only one subnet per component is supported for now. Taking first and ignoring others.')

            subnet_definition = component_value.subnets[0]
            subnet = select_first(infrastructure, lambda item: item.kind == 'infrastructure/subnet' and
                                    item.specification.cidr_block == subnet_definition['address_pool'])
            security_group = select_first(infrastructure, lambda item: item.kind == 'infrastructure/security-group' and
                                            item.specification.cidr_block == subnet_definition['address_pool'])

            if subnet is None:
                subnet = self.get_subnet(subnet_definition, component_key, vpc_name, 0)
                infrastructure.append(subnet)

                if vm_config.specification.mount_efs:
                    self.efs_add_mount_target_config(efs_config, subnet)

                route_table_association = self.get_route_table_association(route_table.specification.name,
                                                                             component_key,
                                                                             subnet.specification.name, 0)
                infrastructure.append(route_table_association)

                if self.use_network_security_groups:
                    security_group = self.get_security_group(subnet, component_key, vpc_name, 0)
                    for rule in vm_config.specification.security.rules:
                        if not self.rule_exists_in_list(security_group.specification.rules, rule):
                            security_group.specification.rules.append(rule)
                    infrastructure.append(security_group)

            for index in range(vm_count):
                vm = self.get_vm(component_key,
                                 vm_config,
                                 subnet,
                                 public_key_config,
                                 security_group,
                                 index)
                infrastructure.append(vm)

        if self.has_efs_any_mounts(efs_config):
            infrastructure.append(efs_config)
            self.add_security_rules_inbound_efs(infrastructure, default_security_group)

        return infrastructure

    def get_resource_group(self):
        resource_group = self.get_config_or_default(self.docs, 'infrastructure/resource-group')
        resource_group.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'rg')
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
        sg_config.specification.cluster_name = self.cluster_name
        return sg_config

    def get_efs_config(self):
        efs_config = self.get_config_or_default(self.docs, 'infrastructure/efs-storage')
        efs_config.specification.token = "aws-efs-token-" + self.cluster_name
        efs_config.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'efs')
        efs_config.specification.cluster_name = self.cluster_name
        return efs_config

    def get_vm(self, component_key, vm_config, subnet, public_key_config, security_group, index):
        vm = dict_to_objdict(deepcopy(vm_config))
        vm.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'vm' + '-' + str(index), component_key)
        vm.specification.cluster_name = self.cluster_name
        vm.specification.component_key = component_key
        vm.specification.subnet_name = subnet.specification.name
        vm.specification.key_name = public_key_config.specification.key_name
        vm.specification.use_network_security_groups = self.use_network_security_groups
        vm.specification.availability_zone = subnet.specification.availability_zone
        if self.use_network_security_groups:
            vm.specification.security_groups = [security_group.specification.name]
        vm.specification.associate_public_ip = self.cluster_model.specification.cloud.use_public_ips
        with APIProxy(self.cluster_model, []) as proxy:
            vm.specification.image_id = proxy.get_image_id(vm.specification.os_full_name)
        return vm

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
            key_pair = select_first(tfstate['resources'], lambda x: x['type'] == 'aws_key_pair')
            public_key_config.specification.key_name = key_pair['instances'][0]['attributes']['id']
        else:
            public_key_config.specification.key_name = self.cluster_model.specification.admin_user.name + '-' \
                                                       + str(uuid.uuid4())
        pub_key_path = self.cluster_model.specification.admin_user.key_path + '.pub'
        if os.path.isfile(pub_key_path):
            with open(pub_key_path, 'r') as stream:
                public_key_config.specification.public_key = stream.read().rstrip()
        else:
            raise Exception(f'SSH key path "{pub_key_path}" is not valid. Ansible run will fail.')
        return public_key_config

    def add_security_rules_inbound_efs(self, infrastructure, security_group):
        vms_allowed_to_efs = select_all(infrastructure, lambda item: item.kind == 'infrastructure/virtual-machine' and
                                                      item.specification.authorized_to_efs)

        for vm in vms_allowed_to_efs:
            subnet = select_single(infrastructure, lambda item: item.kind == 'infrastructure/subnet' and
                                                                item.specification.name == vm.specification.subnet_name)

            rule_defined = select_first(security_group.specification.rules, lambda item: item.source_address_prefix == subnet.specification.cidr_block
                                                                                        and item.destination_port_range == 2049)
            if rule_defined is None:
                rule = self.get_config_or_default(self.docs, 'infrastructure/security-group-rule')
                rule.specification.name = 'sg-rule-nfs-default-from-'+subnet.specification.name
                rule.specification.description = 'NFS inbound for '+subnet.specification.name
                rule.specification.direction = 'ingress'
                rule.specification.protocol = 'tcp'
                rule.specification.destination_port_range = "2049"
                rule.specification.source_address_prefix = subnet.specification.cidr_block
                rule.specification.destination_address_prefix = '*'
                security_group.specification.rules.append(rule.specification)

        rules = []
        for rule in security_group.specification.rules:
            rules.append(objdict_to_dict(rule))
        security_group.specification.rules = rules

    def get_virtual_machine(self, component_value):
        machine_selector = component_value.machine
        model_with_defaults = select_first(self.docs, lambda x: x.kind == 'infrastructure/virtual-machine' and
                                                                 x.name == machine_selector)

        # Merge with defaults
        if model_with_defaults is None:
            model_with_defaults = merge_with_defaults(self.cluster_model.provider, 'infrastructure/virtual-machine',
                                                      machine_selector, self.docs)

        # Check if we have a cluster-config OS image defined that we want to apply cluster wide.
        cloud_os_image_defaults = self.get_config_or_default(self.docs, 'infrastructure/cloud-os-image-defaults')
        cloud_image = self.cluster_model.specification.cloud.default_os_image
        if cloud_image != 'default':
            if not hasattr(cloud_os_image_defaults.specification, cloud_image):
                raise NotImplementedError(f'default_os_image "{cloud_image}" is unsupported for "{self.cluster_model.provider}" provider.')
            model_with_defaults.specification.os_full_name = cloud_os_image_defaults.specification[cloud_image]

        # finally check if we are trying to re-apply a configuration.
        if self.manifest_docs:
            manifest_vm_config = select_first(self.manifest_docs, lambda x: x.name == machine_selector and x.kind == 'infrastructure/virtual-machine')
            manifest_firstvm_config = select_first(self.manifest_docs, lambda x: x.kind == 'infrastructure/virtual-machine')

            if manifest_vm_config  is not None and model_with_defaults.specification.os_full_name == manifest_vm_config.specification.os_full_name:
                return model_with_defaults

            if model_with_defaults.specification.os_full_name == manifest_firstvm_config.specification.os_full_name:
                return model_with_defaults

            self.logger.warning(f"Re-applying a different OS image might lead to data loss and/or other issues. Preserving the existing OS image used for VM definition '{machine_selector}'.")

            if manifest_vm_config  is not None:
                model_with_defaults.specification.os_full_name = manifest_vm_config.specification.os_full_name
            else:
                model_with_defaults.specification.os_full_name = manifest_firstvm_config.specification.os_full_name

        return model_with_defaults


    @staticmethod
    def efs_add_mount_target_config(efs_config, subnet):
        efs_config.specification.mount_targets.append(
            {'name': 'efs-'+subnet.specification.name+'-mount',
             'subnet_name': subnet.specification.name})


    @staticmethod
    def has_efs_any_mounts(efs_config):
        if len(efs_config.specification.mount_targets) > 0:
            return True
        return False


    @staticmethod
    def get_config_or_default(docs, kind):
        config = select_first(docs, lambda x: x.kind == kind)
        if config is None:
            config = load_schema_obj(schema_types.DEFAULT, 'aws', kind)
            config['version'] = VERSION
        return config


    @staticmethod
    def rule_exists_in_list(rule_list, rule_to_check):
        for rule in rule_list:
            if (rule.direction.lower()                  == rule_to_check.direction.lower() and
               rule.protocol.lower()                    == rule_to_check.protocol.lower() and
               rule.destination_port_range.lower()      == rule_to_check.destination_port_range.lower() and
               rule.source_address_prefix.lower()       == rule_to_check.source_address_prefix.lower() and
               rule.destination_address_prefix.lower()  == rule_to_check.destination_address_prefix.lower()):
                return True
        return False
