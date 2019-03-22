from cli.engine.aws.AWSConfigBuilder import AWSConfigBuilder
from cli.helpers.objdict_helpers import dict_to_objdict


def test_get_vpc_config_should_set_address_pool_from_cluster_data_model():
    cluster_model = get_cluster_model(address_pool="10.20.0.0/22")
    builder = AWSConfigBuilder()

    actual = builder.get_vpc_config(cluster_model, None)

    assert actual.specification.address_pool == "10.20.0.0/22"


def test_get_vpc_config_should_set_name_from_cluster_data_model():
    cluster_model = get_cluster_model(cluster_name="TestCluster")
    builder = AWSConfigBuilder()

    actual = builder.get_vpc_config(cluster_model, None)

    assert actual.specification.name == "aws-vpc-testcluster"


def test_get_subnet_config_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name="TestCluster")
    component_value = dict_to_objdict({
        'subnet_address_pool': '10.20.0.0/24'
    })
    builder = AWSConfigBuilder()

    actual = builder.get_subnet(cluster_model, component_value, 1, None, "my-test-vpc")

    assert actual.specification.name == "aws-subnet-testcluster-1"
    assert actual.specification.vpc_name == "my-test-vpc"
    assert actual.specification.cidr_block == "10.20.0.0/24"


def test_get_security_group_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name="TestCluster")
    subnet = dict_to_objdict({
        'specification': {
            'cidr_block': "10.21.0.0/24"
        }
    })
    builder = AWSConfigBuilder()

    actual = builder.get_security_group(cluster_model, subnet, 12, None, "my-test-vpc")

    assert actual.specification.name == "aws-security-group-testcluster-12"
    assert actual.specification.vpc_name == "my-test-vpc"
    assert actual.specification.cidr_block == "10.21.0.0/24"


def test_get_autoscaling_group_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name="TestCluster")
    component_value = dict_to_objdict({
        'machine': "default",
        'count': 4
    })
    builder = AWSConfigBuilder()

    actual = builder.get_autoscaling_group(cluster_model, "TestComponent", component_value, "my-test-subnet", None)

    assert actual.specification.name == "aws-asg-testcluster-testcomponent"
    assert actual.specification.count == 4
    assert actual.specification.subnet == "my-test-subnet"
    assert {'feature': 'TestComponent'} in actual["specification"]["tags"]


def test_get_launch_configuration_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name="TestCluster")
    autoscaling_group = dict_to_objdict({
        'specification': {
            'image_id': "test-image-id",
            'size': "t2.micro.test"
        }
    })
    builder = AWSConfigBuilder()

    actual = builder.get_launch_configuration(autoscaling_group, cluster_model, "TestComponent", "aws-security-group-test", None)

    assert actual.specification.name == "aws-launch-config-testcluster-testcomponent"
    assert actual.specification.size == "t2.micro.test"
    assert actual.specification.image_id == "test-image-id"
    assert actual.specification.security_groups == ["aws-security-group-test"]


def test_get_routing_table_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name="TestCluster")

    builder = AWSConfigBuilder()

    actual = builder.get_routing_table(cluster_model, None, "test-vpc-name", "test-internet-gateway")

    assert actual.specification.name == "aws-route-table-testcluster"
    assert actual.specification.vpc_name == "test-vpc-name"
    assert actual.specification.route.gateway_name == "test-internet-gateway"


def test_get_internet_gateway_should_set_proper_values_to_model():
    cluster_model = get_cluster_model(cluster_name="TestCluster")

    builder = AWSConfigBuilder()

    actual = builder.get_internet_gateway(cluster_model, None, 'test-vpc-name')

    assert actual.specification.name == "aws-internet-gateway-testcluster"
    assert actual.specification.vpc_name == "test-vpc-name"


def get_cluster_model(address_pool="10.22.0.0/22", cluster_name="EpiphanyTestCluster"):
    cluster_model = dict_to_objdict({
        'provider': "aws",
        'specification': {
            'name': cluster_name,
            'cloud': {
                'vnet_address_pool': address_pool
            }
        }
    })
    return cluster_model

