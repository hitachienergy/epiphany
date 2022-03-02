from pytest_mock import MockerFixture

from cli.src.models.AnsibleHostModel import AnsibleOrderedHostModel
from cli.src.providers.any.APIProxy import APIProxy
from tests.unit.providers.data.APIProxy_data import CLUSTER_MODEL, CONFIG_DOC


def test_get_ips_for_feature(mocker: MockerFixture):
    """
    Make sure that hostnames in inventory are sorted.
    """

    mocker.patch('cli.src.providers.any.APIProxy.Log')
    proxy = APIProxy(CLUSTER_MODEL('any'), CONFIG_DOC())

    EXPECTED_RESULT = [
        AnsibleOrderedHostModel('service-vm-0', '20.73.105.240'),
        AnsibleOrderedHostModel('service-vm-1', '20.73.105.188'),
        AnsibleOrderedHostModel('service-vm-2', '20.73.105.18'),
        AnsibleOrderedHostModel('service-vm-3', '20.73.105.33'),
        AnsibleOrderedHostModel('service-vm-4', '20.73.105.54')
    ]

    result = proxy.get_ips_for_feature('service')

    assert EXPECTED_RESULT == result
