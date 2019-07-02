from cli.engine.aws.InfrastructureBuilder import InfrastructureBuilder
from cli.helpers.objdict_helpers import dict_to_objdict
import pytest


def test_get_vpc_config_should_set_address_pool_from_cluster_data_model():
    cluster_model = get_cluster_model(address_pool='10.20.0.0/22')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_vpc_config()

    assert actual.specification.address_pool == '10.20.0.0/22'


def test_get_vpc_config_should_set_name_from_cluster_data_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_vpc_config()

    assert actual.specification.name == 'prefix-testcluster-vpc'


def test_get_subnet_config_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    component_value = dict_to_objdict({
        'address_pool': '10.20.0.0/24',
        'availability_zone': 'eu-west-2a'
    })
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_subnet(component_value, 'component', 'my-test-vpc', 1,)

    assert actual.specification.name == 'prefix-testcluster-component-subnet-1'
    assert actual.specification.vpc_name == 'my-test-vpc'
    assert actual.specification.cidr_block == '10.20.0.0/24'
    assert actual.specification.availability_zone == 'eu-west-2a'


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

@pytest.mark.skip(reason='Rewrite this test regarding subnets')
def test_get_autoscaling_group_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    component_value = dict_to_objdict({
        'machine': 'default',
        'count': 4
    })
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_autoscaling_group('TestComponent', component_value, 'my-test-subnet')

    assert actual.specification.name == 'prefix-testcluster-testcomponent-asg'
    assert actual.specification.count == 4
    assert actual.specification.subnet == 'my-test-subnet'
    #assert {'feature': 'TestComponent'} in actual['specification']['tags'] TODO: check this

@pytest.mark.skip(reason='Rewrite this test regarding security groups')
def test_get_launch_configuration_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    autoscaling_group = dict_to_objdict({
        'specification': {
            'size': 't2.micro.test'
        }
    })
    security_groups_to_create = dict_to_objdict({
        'specification': {
            'name': 'aws-security-group-test'
        }
    })
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_launch_configuration(autoscaling_group, 'TestComponent', security_groups_to_create)

    assert actual.specification.name == 'prefix-testcluster-testcomponent-launch-config'
    assert actual.specification.size == 't2.micro.test'
    assert actual.specification.security_groups == ['aws-security-group-test']


def test_get_routing_table_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')

    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_routing_table('test-vpc-name', 'test-internet-gateway')

    assert actual.specification.name == 'prefix-testcluster-route-table'
    assert actual.specification.vpc_name == 'test-vpc-name'
    assert actual.specification.route.gateway_name == 'test-internet-gateway'


def test_get_internet_gateway_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')

    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_internet_gateway('test-vpc-name')

    assert actual.specification.name == 'prefix-testcluster-internet-gateway'
    assert actual.specification.vpc_name == 'test-vpc-name'


def get_cluster_model(address_pool='10.22.0.0/22', cluster_name='EpiphanyTestCluster'):
    cluster_model = dict_to_objdict({
        'kind': 'epiphany-cluster',
        'provider': 'aws',
        'specification': {
            'name': cluster_name,
            'prefix': 'prefix',
            'cloud': {
                'vnet_address_pool': address_pool
            }
        }
    })
    return cluster_model

