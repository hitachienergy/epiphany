import os
import uuid
from copy import deepcopy

from cli.helpers.Step import Step
from cli.helpers.naming_helpers import resource_name, cluster_tag, storage_account_name
from cli.helpers.doc_list_helpers import select_single, select_all
from cli.helpers.doc_list_helpers import select_first
from cli.helpers.data_loader import load_yaml_obj, types
from cli.helpers.config_merger import merge_with_defaults
from cli.helpers.objdict_helpers import objdict_to_dict, dict_to_objdict
from cli.version import VERSION

class InfrastructureBuilder(Step):
    def __init__(self, docs):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.cluster_name = self.cluster_model.specification.name.lower()
        self.cluster_prefix = self.cluster_model.specification.prefix.lower()
        self.resource_group_name = resource_name(self.cluster_prefix, self.cluster_name, 'rg')
        self.region = self.cluster_model.specification.cloud.region
        self.use_network_security_groups = self.cluster_model.specification.cloud.network.use_network_security_groups
        self.use_public_ips = self.cluster_model.specification.cloud.use_public_ips
        self.docs = docs

    def run(self):
        infrastructure = []

        resource_group = self.get_resource_group()
        infrastructure.append(resource_group)

        vnet = self.get_virtual_network()
        infrastructure.append(vnet)

        shared_storage = self.get_storage_share_config()
        infrastructure.append(shared_storage)

        for component_key, component_value in self.cluster_model.specification.components.items():
            vm_count = component_value['count']
            if vm_count < 1:
                continue

            # The vm config also contains some other stuff we use for network and security config.
            # So get it here and pass it allong.
            vm_config = self.get_virtual_machine(component_value, self.cluster_model, self.docs)

            # If there are no security groups Ansible provisioning will fail because
            # SSH is not allowed then with public IPs on Azure.
            if not(self.use_network_security_groups) and self.use_public_ips:
                 self.logger.warning('Use of security groups has been disabled and public IP are used. Ansible run will fail because SSH will not be allowed.')

            # For now only one subnet per component.
            if (len(component_value.subnets) > 1):
                self.logger.warning(f'On Azure only one subnet per component is supported for now. Taking first and ignoring others.')

            # Add message for ignoring availabiltity zones if present.
            if 'availability_zone' in component_value.subnets[0]:
                self.logger.warning(f'On Azure availability_zones are not supported yet. Ignoring definition.')

            subnet_definition = component_value.subnets[0]
            subnet = select_first(infrastructure, lambda item: item.kind == 'infrastructure/subnet' and
                                    item.specification.address_prefix == subnet_definition['address_pool'])

            if subnet is None:
                subnet = self.get_subnet(subnet_definition, component_key, 0)
                infrastructure.append(subnet)

                if self.use_network_security_groups:
                    nsg = self.get_network_security_group(component_key,
                                                            vm_config.specification.security.rules,
                                                            0)
                    infrastructure.append(nsg)

                    subnet_nsg_association = self.get_subnet_network_security_group_association(component_key,
                                                                                        subnet.specification.name,
                                                                                        nsg.specification.name,
                                                                                        0)
                    infrastructure.append(subnet_nsg_association)

            availability_set = None
            if 'availability_set' in component_value:
                availability_set = select_first(
                    infrastructure,
                    lambda item: item.kind == 'infrastructure/availability-set' and item.name == component_value.availability_set,
                )
                if availability_set is None:
                    availability_set = self.get_availability_set(component_value.availability_set)
                    if availability_set is not None:
                        infrastructure.append(availability_set)

            #TODO: For now we create the VM infrastructure compatible with the Epiphany 2.x
            #      code line but later we might want to look at scale sets to achieve the same result:
            #      https://www.terraform.io/docs/providers/azurerm/r/virtual_machine_scale_set.html
            for index in range(vm_count):
                public_ip_name = ''
                if self.cluster_model.specification.cloud.use_public_ips:
                    public_ip = self.get_public_ip(component_key,
                                                   component_value,
                                                   vm_config,
                                                   index)
                    infrastructure.append(public_ip)
                    public_ip_name = public_ip.specification.name

                if self.use_network_security_groups:
                    nsg_name = nsg.specification.name
                else:
                    nsg_name = ''

                network_interface = self.get_network_interface(component_key,
                                                               component_value,
                                                               vm_config,
                                                               subnet.specification.name,
                                                               nsg_name,
                                                               public_ip_name,
                                                               index)
                infrastructure.append(network_interface)

                vm = self.get_vm(component_key, component_value, vm_config, availability_set,
                                 network_interface.specification.name, index)
                infrastructure.append(vm)

        return infrastructure

    def get_resource_group(self):
        resource_group = self.get_config_or_default(self.docs, 'infrastructure/resource-group')
        resource_group.specification.name = self.resource_group_name
        resource_group.specification.region = self.cluster_model.specification.cloud.region
        return resource_group

    def get_virtual_network(self):
        vnet = self.get_config_or_default(self.docs, 'infrastructure/vnet')
        vnet.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'vnet')
        vnet.specification.address_space = self.cluster_model.specification.cloud.vnet_address_pool
        return vnet

    def get_network_security_group(self, component_key, security_rules,  index):
        security_group = self.get_config_or_default(self.docs, 'infrastructure/network-security-group')
        security_group.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'nsg' + '-' + str(index), component_key)
        security_group.specification.rules = security_rules
        return security_group

    def get_subnet(self, subnet_definition, component_key, index):
        subnet = self.get_config_or_default(self.docs, 'infrastructure/subnet')
        subnet.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'subnet' + '-' + str(index), component_key)
        subnet.specification.address_prefix = subnet_definition['address_pool']
        subnet.specification.cluster_name = self.cluster_name
        return subnet

    def get_availability_set(self, availability_set_name):
        availability_set = select_first(
            self.docs,
            lambda item: item.kind == 'infrastructure/availability-set' and item.name == availability_set_name,
        )
        if availability_set is not None:
            availability_set.specification.name = resource_name(self.cluster_prefix, self.cluster_name, availability_set_name + '-' + 'aset')
        return availability_set

    def get_subnet_network_security_group_association(self, component_key, subnet_name, security_group_name, index):
        ssga = self.get_config_or_default(self.docs, 'infrastructure/subnet-network-security-group-association')
        ssga.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'ssga' + '-' + str(index), component_key)
        ssga.specification.subnet_name = subnet_name
        ssga.specification.security_group_name = security_group_name
        return ssga

    def get_network_interface(self, component_key, component_value, vm_config, subnet_name, security_group_name, public_ip_name, index):
        network_interface = self.get_config_or_default(self.docs, 'infrastructure/network-interface')
        network_interface.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'nic' + '-' + str(index), component_key)
        network_interface.specification.use_network_security_groups = self.use_network_security_groups
        network_interface.specification.security_group_name = security_group_name
        network_interface.specification.ip_configuration_name = resource_name(self.cluster_prefix, self.cluster_name, 'ipconf' + '-' + str(index), component_key)
        network_interface.specification.subnet_name = subnet_name
        network_interface.specification.use_public_ip = self.cluster_model.specification.cloud.use_public_ips
        network_interface.specification.public_ip_name = public_ip_name
        network_interface.specification.enable_accelerated_networking = vm_config.specification.network_interface.enable_accelerated_networking
        return network_interface

    def get_public_ip(self, component_key, component_value, vm_config, index):
        public_ip = self.get_config_or_default(self.docs, 'infrastructure/public-ip')
        public_ip.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'pubip' + '-' + str(index), component_key)
        public_ip.specification.allocation_method = vm_config.specification.network_interface.public_ip.allocation_method
        public_ip.specification.idle_timeout_in_minutes = vm_config.specification.network_interface.public_ip.idle_timeout_in_minutes
        public_ip.specification.sku = vm_config.specification.network_interface.public_ip.sku
        return public_ip

    def get_storage_share_config(self):
        storage_share = self.get_config_or_default(self.docs, 'infrastructure/storage-share')
        storage_share.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'k8s-ss')
        storage_share.specification.storage_account_name = storage_account_name(self.cluster_prefix, self.cluster_name, 'k8s')
        return storage_share

    def get_vm(self, component_key, component_value, vm_config, availability_set, network_interface_name, index):
        vm = dict_to_objdict(deepcopy(vm_config))
        vm.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'vm' + '-' + str(index), component_key)
        vm.specification.admin_username = self.cluster_model.specification.admin_user.name
        vm.specification.network_interface_name = network_interface_name
        vm.specification.tags.append({'cluster': cluster_tag(self.cluster_prefix, self.cluster_name)})
        vm.specification.tags.append({component_key: ''})
        if vm_config.specification.os_type == 'windows':
            raise NotImplementedError('Windows VMs not supported jet.')
        pub_key_path = self.cluster_model.specification.admin_user.key_path + '.pub'
        if os.path.isfile(pub_key_path):
            vm.specification.public_key = pub_key_path
        else:
            raise Exception(f'SSH key path "{pub_key_path}" is not valid. Ansible run will fail.')
        if availability_set is not None:
            vm.specification.availability_set_name = availability_set.specification.name
        return vm

    @staticmethod
    def get_config_or_default(docs, kind):
        config = select_first(docs, lambda x: x.kind == kind)
        if config is None:
            config = load_yaml_obj(types.DEFAULT, 'azure', kind)
            config['version'] = VERSION
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
