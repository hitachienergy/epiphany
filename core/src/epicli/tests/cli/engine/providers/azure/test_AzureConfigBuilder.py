from cli.engine.providers.azure.InfrastructureBuilder import InfrastructureBuilder
from cli.helpers.objdict_helpers import dict_to_objdict
import pytest


def test_get_resource_group_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_resource_group()

    assert actual.specification.name == 'prefix-testcluster-rg'
    assert actual.specification.region == 'West Europe'


def test_get_virtual_network_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name='TestCluster')
    builder = InfrastructureBuilder([cluster_model])

    actual = builder.get_virtual_network()

    assert actual.specification.name == 'prefix-testcluster-vnet'
    assert actual.specification.address_space == '10.22.0.0/22'


def get_cluster_model(address_pool='10.22.0.0/22', cluster_name='EpiphanyTestCluster'):
    cluster_model = dict_to_objdict({
        'kind': 'epiphany-cluster',
        'provider': 'azure',
        'specification': {
            'name': cluster_name,
            'prefix': 'prefix',
            'cloud': {
                'region': 'West Europe',
                'vnet_address_pool': address_pool
            }
        }
    })
    return cluster_model

