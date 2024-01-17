from cli.src.helpers.objdict_helpers import dict_to_objdict
from cli.src.providers.azure.InfrastructureBuilder import InfrastructureBuilder


def test_get_resource_group_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_resource_group()

    assert actual.specification.name == 'testcluster-rg'
    assert actual.specification.region == 'West Europe'


def test_get_virtual_network_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_virtual_network()

    assert actual.specification.name == 'testcluster-vnet'
    assert actual.specification.address_space == '10.22.0.0/22'


def test_get_network_security_group_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_network_security_group('component', [])

    assert actual.specification.name == 'testcluster-component-nsg'


def test_get_subnet_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    subnet_definition = dict_to_objdict({
        'address_pool': '10.20.0.0/24'
    })
    builder = InfrastructureBuilder([cluster_model])
    actual = builder.get_subnet(subnet_definition, 'component')

    assert actual.specification.name == 'component-snet'
    assert actual.specification.address_prefix == subnet_definition['address_pool']
    assert actual.specification.cluster_name == 'testcluster'


def test_get_availability_set_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    availability_set = dict_to_objdict({
        'kind': 'infrastructure/availability-set',
        'provider': 'azure',
        'name': 'availability-set',
        'specification': {
            'name': 'availability-set'
        }
    })

    builder = InfrastructureBuilder([cluster_model, availability_set])

    actual = builder.get_availability_set('availability-set')

    assert actual.name == 'availability-set'
    assert actual.specification.name == 'testcluster-availability-set-avail'


def test_get_subnet_network_security_group_association_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_subnet_network_security_group_association(
                                'testcluster-component-subnet-1',
                                'testcluster-component-sg-1')

    assert actual.specification.name == 'testcluster-component-subnet-1-nsga'
    assert actual.specification.subnet_name == 'testcluster-component-subnet-1'
    assert actual.specification.security_group_name == 'testcluster-component-sg-1'


def test_get_network_interface_security_group_association_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_network_interface_security_group_association(
                                'testcluster-component-nic-1',
                                'testcluster-component-sg-1')

    assert actual.specification.name == 'testcluster-component-nic-1-nsga'
    assert actual.specification.network_interface_name == 'testcluster-component-nic-1'
    assert actual.specification.security_group_name == 'testcluster-component-sg-1'


def test_get_network_interface_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])
    component_value = dict_to_objdict({
        'machine': 'repository-machine'
    })
    vm_config = builder.get_virtual_machine(component_value)

    actual = builder.get_network_interface(
                                'repository-01',
                                vm_config,
                                'testcluster-component-subnet-1',
                                'testcluster-repository-pubip-1',
                                'testcluster-component-sga-1')

    assert actual.specification.name == 'repository-01-nic'
    assert actual.specification.security_group_association_name == 'testcluster-component-sga-1'
    assert actual.specification.ip_configuration_name == 'repository-01-nic-ipconf-01'
    assert actual.specification.subnet_name == 'testcluster-component-subnet-1'
    assert actual.specification.use_public_ip is True
    assert actual.specification.public_ip_name == 'testcluster-repository-pubip-1'
    assert actual.specification.enable_accelerated_networking is True


def test_get_public_ip_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])
    component_value = dict_to_objdict({
        'machine': 'repository-machine'
    })
    vm_config = builder.get_virtual_machine(component_value)

    actual = builder.get_public_ip('repository', vm_config, 1)

    assert actual.specification.name == 'testcluster-repository-pubip-1'
    assert actual.specification.allocation_method == 'Static'
    assert actual.specification.idle_timeout_in_minutes == 30
    assert actual.specification.sku == 'Standard'


def get_cluster_model(address_pool='10.22.0.0/22', cluster_name='EpiphanyTestCluster'):
    cluster_model = dict_to_objdict({
        'kind': 'epiphany-cluster',
        'provider': 'azure',
        'name': 'default',
        'specification': {
            'name': cluster_name,
            'cloud': {
                'region': 'West Europe',
                'vnet': {
                    'use_managed': True,
                    'managed': {
                        'address_pool': address_pool
                    }
                },
                'use_public_ips': True,
                'default_os_image': 'default',
                'hostname_domain_extension': '',
                'network': {
                    'use_network_security_groups': True
                }
            }
        }
    })
    return cluster_model

