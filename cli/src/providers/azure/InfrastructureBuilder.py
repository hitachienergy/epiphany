import os
from copy import deepcopy

from cli.src.helpers.config_merger import merge_with_defaults
from cli.src.helpers.data_loader import load_schema_obj, schema_types
from cli.src.helpers.doc_list_helpers import select_first, select_single
from cli.src.helpers.naming_helpers import (cluster_tag,
                                            get_os_name_normalized,
                                            resource_name)
from cli.src.helpers.objdict_helpers import dict_to_objdict
from cli.src.Step import Step
from cli.version import VERSION

HOST_NAME_MAX_LENGTH = 63


class InfrastructureBuilder(Step):
    def __init__(self, docs, manifest_docs=[]):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.cluster_name = self.cluster_model.specification.name.lower()
        self.cluster_prefix = None
        self.resource_group_name = resource_name(self.cluster_prefix, self.cluster_name, 'rg')
        self.region = self.cluster_model.specification.cloud.region
        self.use_network_security_groups = self.cluster_model.specification.cloud.network.use_network_security_groups
        self.use_public_ips = self.cluster_model.specification.cloud.use_public_ips
        self.docs = docs
        self.manifest_docs = manifest_docs

        # If there are no security groups Ansible provisioning will fail because
        # SSH is not allowed then with public IPs on Azure.
        if not(self.use_network_security_groups) and self.use_public_ips:
            self.logger.warning('Use of security groups has been disabled and public IPs are used. Ansible run will fail because SSH will not be allowed.')

        # Check if there is a hostname_domain_extension we already applied and we want to retain.
        # The same as VM images we want to preserve hostname_domain_extension over versions.
        self.hostname_domain_extension = self.cluster_model.specification.cloud.hostname_domain_extension
        manifest_cluster_model = select_first(self.manifest_docs, lambda x: x.kind == 'epiphany-cluster')
        if self.manifest_docs:
            if 'hostname_domain_extension' in manifest_cluster_model.specification.cloud:
                old_hostname_domain_extension = manifest_cluster_model.specification.cloud.hostname_domain_extension
                if old_hostname_domain_extension != self.hostname_domain_extension:
                    self.logger.warning(f"Re-applying a different hostname_domain_extension might lead to data loss and/or other issues. Preserving the previous hostname_domain_extension: '{old_hostname_domain_extension}'.")
                    self.cluster_model.specification.cloud.hostname_domain_extension = old_hostname_domain_extension
                    self.hostname_domain_extension = old_hostname_domain_extension

    def run(self):
        infrastructure = []

        resource_group = self.get_resource_group()
        infrastructure.append(resource_group)

        vnet = self.get_virtual_network()
        infrastructure.append(vnet)

        cloud_init_custom_data = self.get_cloud_init_custom_data()

        for component_key, component_value in self.cluster_model.specification.components.items():
            vm_count = component_value['count']
            if vm_count < 1:
                continue

            # The vm config also contains some other stuff we use for network and security config.
            # So get it here and pass it allong.
            vm_config = self.get_virtual_machine(component_value)
            # Set property that controls cloud-init.
            vm_config.specification['use_cloud_init_custom_data'] = cloud_init_custom_data.specification.enabled

            subnet_definition = component_value.subnet
            subnet = select_first(infrastructure, lambda item: item.kind == 'infrastructure/subnet' and
                                  item.specification.address_prefix == subnet_definition['address_pool'])

            if subnet is None:
                subnet_nsg_association_name = ''
                subnet = self.get_subnet(subnet_definition, component_key)
                infrastructure.append(subnet)

                if self.use_network_security_groups:
                    nsg = self.get_network_security_group(component_key,
                                                          vm_config.specification.security.rules)

                    infrastructure.append(nsg)
                    subnet_nsg_association = self.get_subnet_network_security_group_association(
                                                subnet.specification.name,
                                                nsg.specification.name
                                             )
                    infrastructure.append(subnet_nsg_association)
                    subnet_nsg_association_name = subnet_nsg_association.specification.name

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

            for index in range(vm_count):
                public_ip_name = ''
                if self.cluster_model.specification.cloud.use_public_ips:
                    public_ip = self.get_public_ip(component_key,
                                                   vm_config,
                                                   index)
                    infrastructure.append(public_ip)
                    public_ip_name = public_ip.specification.name

                vm_name = self.__get_vm_name(component_key, component_value['alt_component_name'], self.__normalize_index(index))

                network_interface = self.get_network_interface(vm_name,
                                                               vm_config,
                                                               subnet.specification.name,
                                                               public_ip_name,
                                                               subnet_nsg_association_name)
                infrastructure.append(network_interface)

                security_group_association_name = ''
                if self.use_network_security_groups:
                    nic_nsg_association = self.get_network_interface_security_group_association(
                                              network_interface.specification.name,
                                              nsg.specification.name
                                          )
                    infrastructure.append(nic_nsg_association)
                    security_group_association_name = nic_nsg_association.specification.name

                vm = self.get_vm(component_key,
                                 component_value['alt_component_name'],
                                 vm_config,
                                 availability_set,
                                 network_interface.specification.name,
                                 security_group_association_name,
                                 self.__normalize_index(index),
                                 vm_name)
                infrastructure.append(vm)

        first_vm_doc = select_first(infrastructure, lambda x: x.kind == 'infrastructure/virtual-machine')
        if first_vm_doc is not None:
            cloud_init_custom_data.specification['os_distribution'] = get_os_name_normalized(first_vm_doc)

        infrastructure.append(cloud_init_custom_data)

        return infrastructure

    def get_resource_group(self):
        resource_group = self.get_config_or_default(self.docs, 'infrastructure/resource-group')
        resource_group.specification.use_managed = self.cluster_model.specification.cloud.vnet.use_managed
        if resource_group.specification.use_managed is True:
            resource_group.specification.name = self.resource_group_name
        else:
            resource_group.specification.name = self.cluster_model.specification.cloud.vnet.unmanaged.resource_group_name
        resource_group.specification.region = self.cluster_model.specification.cloud.region
        return resource_group

    def get_virtual_network(self):
        vnet = self.get_config_or_default(self.docs, 'infrastructure/vnet')
        if self.cluster_model.specification.cloud.vnet.use_managed is True:
            vnet.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'vnet')
        else:
            vnet.specification.name = self.cluster_model.specification.cloud.vnet.unmanaged.name
        vnet.specification.address_space = self.cluster_model.specification.cloud.vnet.managed.address_pool
        vnet.specification.use_managed = self.cluster_model.specification.cloud.vnet.use_managed
        return vnet

    def get_network_security_group(self, component_key, security_rules):
        security_group = self.get_config_or_default(self.docs, 'infrastructure/network-security-group')
        security_group.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'nsg', component_key)
        security_group.specification.rules = security_rules
        security_group.specification.use_managed_resource_group = self.cluster_model.specification.cloud.vnet.use_managed
        return security_group

    def get_subnet(self, subnet_definition, component_key):
        subnet = self.get_config_or_default(self.docs, 'infrastructure/subnet')
        subnet.specification.name = f'{component_key}-snet'
        subnet.specification.address_prefix = subnet_definition['address_pool']
        subnet.specification.cluster_name = self.cluster_name
        subnet.specification.service_endpoints = subnet_definition['service_endpoints'] if 'service_endpoints' in subnet_definition else []
        subnet.specification.use_managed = self.cluster_model.specification.cloud.vnet.use_managed
        return subnet

    def get_availability_set(self, availability_set_name):
        availability_set = select_first(
            self.docs,
            lambda item: item.kind == 'infrastructure/availability-set' and item.name == availability_set_name,
        )
        if availability_set is not None:
            availability_set.specification.name = resource_name(self.cluster_prefix, self.cluster_name, availability_set_name + '-' + 'avail')
            availability_set.specification.use_managed_resource_group = self.cluster_model.specification.cloud.vnet.use_managed
        return availability_set

    def get_subnet_network_security_group_association(self, subnet_name, security_group_name):
        ssga = self.get_config_or_default(self.docs, 'infrastructure/subnet-network-security-group-association')
        ssga.specification.name = f'{subnet_name}-nsga'
        ssga.specification.subnet_name = subnet_name
        ssga.specification.security_group_name = security_group_name
        ssga.specification.use_managed_subnet = self.cluster_model.specification.cloud.vnet.use_managed
        return ssga

    def get_network_interface_security_group_association(self, network_interface_name, security_group_name):
        nsga = self.get_config_or_default(self.docs, 'infrastructure/network-interface-security-group-association')
        nsga.specification.name = f'{network_interface_name}-nsga'
        nsga.specification.network_interface_name = network_interface_name
        nsga.specification.security_group_name = security_group_name
        return nsga

    def get_network_interface(self, vm_name, vm_config, subnet_name, public_ip_name, security_group_association_name):
        network_interface = self.get_config_or_default(self.docs, 'infrastructure/network-interface')
        network_interface.specification.name = f'{vm_name}-nic'
        network_interface.specification.use_network_security_groups = self.use_network_security_groups
        network_interface.specification.security_group_association_name = security_group_association_name
        network_interface.specification.ip_configuration_name = network_interface.specification.name + '-ipconf-01'
        network_interface.specification.subnet_name = subnet_name
        network_interface.specification.use_public_ip = self.cluster_model.specification.cloud.use_public_ips
        network_interface.specification.public_ip_name = public_ip_name
        network_interface.specification.enable_accelerated_networking = vm_config.specification.network_interface.enable_accelerated_networking
        network_interface.specification.use_managed_resource_group = self.cluster_model.specification.cloud.vnet.use_managed
        return network_interface

    def get_public_ip(self, component_key, vm_config, index):
        public_ip = self.get_config_or_default(self.docs, 'infrastructure/public-ip')
        public_ip.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'pubip' + '-' + str(index), component_key)
        public_ip.specification.allocation_method = vm_config.specification.network_interface.public_ip.allocation_method
        public_ip.specification.idle_timeout_in_minutes = vm_config.specification.network_interface.public_ip.idle_timeout_in_minutes
        public_ip.specification.sku = vm_config.specification.network_interface.public_ip.sku
        public_ip.specification.use_managed_resource_group = self.cluster_model.specification.cloud.vnet.use_managed
        return public_ip

    def get_vm(self, component_key, alt_component_name, vm_config, availability_set, network_interface_name, security_group_association_name, index, vm_name):
        vm = dict_to_objdict(deepcopy(vm_config))
        vm.specification.name = vm_name
        if self.hostname_domain_extension != '':
            component_name = self.__get_component_name(component_key, alt_component_name)
            vm.specification.hostname = resource_name(self.cluster_prefix, self.cluster_name, f'vm-{index}.{self.hostname_domain_extension}', component_name)
        else:
            vm.specification.hostname = vm.specification.name
        if len(vm.specification.hostname) > HOST_NAME_MAX_LENGTH:
            raise Exception(f'Host name cannot exceed {HOST_NAME_MAX_LENGTH} characters in length, yours is {vm.specification.hostname}. Consider setting alt_component_name property.')
        vm.specification.admin_username = self.cluster_model.specification.admin_user.name
        vm.specification.network_interface_name = network_interface_name
        vm.specification.use_network_security_groups = self.use_network_security_groups
        vm.specification.security_group_association_name = security_group_association_name
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
        vm.specification.use_managed_resource_group = self.cluster_model.specification.cloud.vnet.use_managed
        return vm

    def get_cloud_init_custom_data(self):
        cloud_init_custom_data = self.get_config_or_default(self.docs, 'infrastructure/cloud-init-custom-data')
        cloud_init_custom_data.specification.file_name = 'cloud-config.yml'
        return cloud_init_custom_data

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

            model_with_defaults.specification.storage_image_reference = dict_to_objdict(deepcopy(cloud_os_image_defaults.specification[cloud_image]))

            if 'plan' in cloud_os_image_defaults.specification[cloud_image]:
                model_with_defaults.specification.plan = dict_to_objdict(deepcopy(cloud_os_image_defaults.specification[cloud_image].plan))
                del model_with_defaults.specification.storage_image_reference.plan

        # finally check if we are trying to re-apply a configuration.
        if self.manifest_docs:
            manifest_vm_config = select_first(self.manifest_docs, lambda x: x.name == machine_selector and x.kind == 'infrastructure/virtual-machine')

            if manifest_vm_config is None:
                manifest_vm_config = select_first(self.manifest_docs, lambda x: x.kind == 'infrastructure/virtual-machine')

            if model_with_defaults.specification.storage_image_reference == manifest_vm_config.specification.storage_image_reference:
                if (not 'plan' in manifest_vm_config.specification) or model_with_defaults.specification.plan == manifest_vm_config.specification.plan:
                    return model_with_defaults

            self.logger.warning(f"Re-applying a different OS image might lead to data loss and/or other issues. Preserving the existing OS image used for VM definition '{machine_selector}'.")

            model_with_defaults.specification.storage_image_reference = dict_to_objdict(deepcopy(manifest_vm_config.specification.storage_image_reference))

            if 'plan' in manifest_vm_config.specification:
                model_with_defaults.specification.plan = dict_to_objdict(deepcopy(manifest_vm_config.specification.plan))

        return model_with_defaults

    def __get_component_name(self, component_key, alt_component_name):
        return alt_component_name if alt_component_name and alt_component_name.strip() else component_key

    def __get_vm_name(self, component_key, alt_component_name, index):
        component_name = self.__get_component_name(component_key, alt_component_name)
        return resource_name(self.cluster_prefix, self.cluster_name, f'vm-{index}', component_name)

    @staticmethod
    def get_config_or_default(docs, kind):
        config = select_first(docs, lambda x: x.kind == kind)
        if config is None:
            config = load_schema_obj(schema_types.DEFAULT, 'azure', kind)
            config['version'] = VERSION
        return config

    @staticmethod
    def __normalize_index(index: int):
        index += 1 # 0 -> 1
        return str(index).zfill(2) # 1 -> 01
