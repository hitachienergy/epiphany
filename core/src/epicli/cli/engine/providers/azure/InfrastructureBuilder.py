import os

from cli.helpers.Step import Step
from cli.helpers.naming_helpers import resource_name
from cli.helpers.doc_list_helpers import select_single, select_all
from cli.helpers.doc_list_helpers import select_first
from cli.helpers.data_loader import load_yaml_obj, types
from cli.helpers.config_merger import merge_with_defaults

class InfrastructureBuilder(Step):
    def __init__(self, docs):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.cluster_name = self.cluster_model.specification.name.lower()
        self.cluster_prefix = self.cluster_model.specification.prefix.lower()
        self.resource_group_name = resource_name(self.cluster_prefix, self.cluster_name, 'rg')
        self.region = self.cluster_model.specification.cloud.region
        self.docs = docs

    def run(self):
        infrastructure = []

        resource_group = self.get_resource_group()
        infrastructure.append(resource_group)        

        vnet = self.get_virtual_network()
        infrastructure.append(vnet)

        for component_key, component_value in self.cluster_model.specification.components.items():
            vm_count = component_value['count']
            if vm_count < 1:
                continue

            # For now only one subnet per component.
            if (len(component_value.subnets) > 1):
                self.logger.warning(f'On Azure only one subnet per component is supported for now. Taking first and ignoring others.')    

            subnet_definition = component_value.subnets[0]
            subnet = select_first(infrastructure, lambda item: item.kind == 'infrastructure/subnet' and
                                    item.specification.address_prefix == subnet_definition['address_pool'])

            if subnet is None:
                security_group = self.get_security_group(component_key, 0)
                infrastructure.append(security_group)
            
                subnet = self.get_subnet(subnet_definition, component_key, 0)
                infrastructure.append(subnet)

                ssg_association = self.get_subnet_network_security_group_association(component_key, 
                                                                                     subnet.specification.name, 
                                                                                     security_group.specification.name,
                                                                                     0)
                infrastructure.append(ssg_association) 

            #TODO: For now we create the VM infrastructure compatible with the Epiphany 2.x 
            #      code line but later we might want to look at scale sets to achieve the same result:
            #      https://www.terraform.io/docs/providers/azurerm/r/virtual_machine_scale_set.html
            for index in range(vm_count):
                public_ip_name = ''
                if self.cluster_model.specification.cloud.use_public_ips:
                    public_ip = self.get_public_ip(component_key, 
                                                   component_value, 
                                                   index)
                    infrastructure.append(public_ip)
                    public_ip_name = public_ip.specification.name

                network_interface = self.get_network_interface(component_key, 
                                                               component_value, 
                                                               subnet.specification.name, 
                                                               security_group.specification.name,
                                                               public_ip_name,
                                                               index)
                infrastructure.append(network_interface)

                vm = self.get_vm(component_key, component_value, network_interface.specification.name, index)
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

    def get_security_group(self, component_key, index):
        security_group = self.get_config_or_default(self.docs, 'infrastructure/security-group')
        security_group.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'sg' + '-' + str(index), component_key)
        return security_group       

    def get_subnet(self, subnet_definition, component_key, index):
        subnet = self.get_config_or_default(self.docs, 'infrastructure/subnet')
        subnet.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'subnet' + '-' + str(index), component_key)
        subnet.specification.address_prefix = subnet_definition['address_pool']
        subnet.specification.cluster_name = self.cluster_name
        return subnet     

    def get_subnet_network_security_group_association(self, component_key, subnet_name, security_group_name, index):
        ssg_association = self.get_config_or_default(self.docs, 'infrastructure/subnet-network-security-group-association')
        ssg_association.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'ssga' + '-' + str(index), component_key)
        ssg_association.specification.subnet_name = subnet_name
        ssg_association.specification.security_group_name = security_group_name
        return ssg_association

    def get_network_interface(self, component_key, component_value, subnet_name, security_group_name, public_ip_name, index):
        vm = self.get_virtual_machine(component_value, self.cluster_model, self.docs)
        network_interface = self.get_config_or_default(self.docs, 'infrastructure/network-interface')
        network_interface.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'nic' + '-' + str(index), component_key)
        network_interface.specification.security_group_name = security_group_name
        network_interface.specification.ip_configuration_name = resource_name(self.cluster_prefix, self.cluster_name, 'ipconf' + '-' + str(index), component_key)
        network_interface.specification.subnet_name = subnet_name
        network_interface.specification.use_public_ip = self.cluster_model.specification.cloud.use_public_ips
        network_interface.specification.public_ip_name = public_ip_name
        network_interface.specification.enable_accelerated_networking = vm.specification.network_interface.enable_accelerated_networking
        return network_interface

    def get_public_ip(self, component_key, component_value, index):
        vm = self.get_virtual_machine(component_value, self.cluster_model, self.docs)
        public_ip = self.get_config_or_default(self.docs, 'infrastructure/public-ip')
        public_ip.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'pubip' + '-' + str(index), component_key)
        public_ip.specification.public_ip_address_allocation = vm.specification.network_interface.public_ip.public_ip_address_allocation
        public_ip.specification.idle_timeout_in_minutes = vm.specification.network_interface.public_ip.idle_timeout_in_minutes
        public_ip.specification.sku = vm.specification.network_interface.public_ip.sku
        return public_ip        

    def get_vm(self, component_key, component_value, network_interface_name, index):
        vm = self.get_virtual_machine(component_value, self.cluster_model, self.docs)
        vm.specification.name = resource_name(self.cluster_prefix, self.cluster_name, 'vm' + '-' + str(index), component_key)
        vm.specification.admin_username = self.cluster_model.specification.admin_user.name
        vm.specification.network_interface_name = network_interface_name
        if vm.specification.os_type == 'linux':
            # For linux we dont need a PW since we only support SSH so just add something random.
            vm.specification.admin_password = "NeverGonnaNeed!"
        if vm.specification.os_type == 'windows':
            #TODO: We need PW or can we support SSH or something different on Windows?
            vm.specification.admin_password = 'TODO' 
        pub_key_path = self.cluster_model.specification.admin_user.key_path + '.pub'
        if os.path.isfile(pub_key_path):
            vm.specification.public_key = pub_key_path
        else:
            raise Exception(f'SSH key path "{pub_key_path}" is not valid. Ansible run will fail.')
        return vm                
    
    @staticmethod
    def get_config_or_default(docs, kind):
        config = select_first(docs, lambda x: x.kind == kind)
        if config is None:
            return load_yaml_obj(types.DEFAULT, 'azure', kind)
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

