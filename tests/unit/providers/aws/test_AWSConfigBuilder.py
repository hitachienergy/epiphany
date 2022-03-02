from cli.src.helpers.objdict_helpers import dict_to_objdict
from cli.src.providers.aws.InfrastructureBuilder import InfrastructureBuilder


def test_get_resource_group_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster', address_pool='10.20.0.0/22')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_resource_group()

    assert actual.specification.name == 'prefix-testcluster-rg'
    assert actual.specification.cluster_name == 'testcluster'


def test_get_vpc_config_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster', address_pool='10.20.0.0/22')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_vpc_config()

    assert actual.specification.name == 'prefix-testcluster-vpc'
    assert actual.specification.address_pool == '10.20.0.0/22'


def test_get_default_security_group_config_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster', address_pool='10.20.0.0/22')
    vpc_config = dict_to_objdict({
        'specification': {
            'name': 'prefix-testcluster-vpc'
        }
    })
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_default_security_group_config(vpc_config)

    assert actual.specification.vpc_name == 'prefix-testcluster-vpc'


def test_get_efs_config_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster', address_pool='10.20.0.0/22')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_efs_config()

    assert actual.specification.token == 'aws-efs-token-testcluster'
    assert actual.specification.name == 'prefix-testcluster-efs'


def test_get_subnet_config_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    component_value = dict_to_objdict({
        'address_pool': '10.20.0.0/24',
        'availability_zone': 'eu-westa'
    })
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_subnet(component_value, 'component', 'my-test-vpc', 1,)

    assert actual.specification.name == 'prefix-testcluster-component-subnet-1'
    assert actual.specification.vpc_name == 'my-test-vpc'
    assert actual.specification.cidr_block == '10.20.0.0/24'
    assert actual.specification.availability_zone == 'eu-westa'


def test_get_security_group_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    subnet = dict_to_objdict({
        'specification': {
            'cidr_block': '10.21.0.0/24'
        }
    })
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_security_group(subnet, 'component', 'my-test-vpc', 1)

    assert actual.specification.name == 'prefix-testcluster-component-security-group-1'
    assert actual.specification.vpc_name == 'my-test-vpc'
    assert actual.specification.cidr_block == '10.21.0.0/24'


def test_get_route_table_association_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_route_table_association('route-table-name','component', 'test-subnet', 1)

    assert actual.specification.name == 'prefix-testcluster-component-1-route-association'
    assert actual.specification.subnet_name  == 'test-subnet'
    assert actual.specification.route_table_name == 'route-table-name'


def test_get_internet_gateway_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')

    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_internet_gateway('test-vpc-name')

    assert actual.specification.name == 'prefix-testcluster-internet-gateway'
    assert actual.specification.vpc_name == 'test-vpc-name'


def test_get_routing_table_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')

    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_routing_table('test-vpc-name', 'test-internet-gateway')

    assert actual.specification.name == 'prefix-testcluster-route-table'
    assert actual.specification.vpc_name == 'test-vpc-name'
    assert actual.specification.route.gateway_name == 'test-internet-gateway'


def get_cluster_model(address_pool='10.22.0.0/22', cluster_name='EpiphanyTestCluster'):
    cluster_model = dict_to_objdict({
        'kind': 'epiphany-cluster',
        'provider': 'aws',
        'specification': {
            'name': cluster_name,
            'prefix': 'prefix',
            'cloud': {
                'vnet_address_pool': address_pool,
                'network': {
                    'use_network_security_groups': True
                },
                'default_os_image': 'default',
                'use_public_ips': True
            }
        }
    })
    return cluster_model
