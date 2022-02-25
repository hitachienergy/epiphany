from pytest_mock import MockerFixture

from cli.src.models.AnsibleHostModel import AnsibleOrderedHostModel
from cli.src.providers.aws.APIProxy import APIProxy
from tests.unit.providers.data.APIProxy_data import (CLUSTER_MODEL,
                                                     RUNNING_INSTANCES_AWS)


def test_get_ips_for_feature(mocker: MockerFixture):
    """
    Make sure that hostnames in inventory are sorted.
    """

    mocker.patch('cli.src.providers.azure.APIProxy.Log')
    mocker.patch('boto3.session.Session')

    # mock proxy with prepared data
    proxy = APIProxy(CLUSTER_MODEL('aws'), [])
    proxy.get_vpc_id = (lambda *args: 'vpc_id')
    proxy.session.resource('ec2').instances.filter = (lambda Filters = []: RUNNING_INSTANCES_AWS)

    EXPECTED_RESULT = [
        AnsibleOrderedHostModel('prefix-cluster-service-vm-0', '20.73.105.240'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-1', '20.73.105.188'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-2', '20.73.105.18'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-3', '20.73.105.33'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-4', '20.73.105.54')
    ]

    result = proxy.get_ips_for_feature('service')

    assert EXPECTED_RESULT == result
