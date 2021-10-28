from unittest import mock, TestCase

from cli.engine.providers.any.APIProxy import APIProxy
from cli.models.AnsibleHostModel import AnsibleOrderedHostModel
from tests.unit.engine.providers.data.APIProxy_data import CLUSTER_MODEL, CONFIG_DOC


class APIProxyTest(TestCase):
    """ Tests for `any` provider """

    def setUp(self):
        self.maxDiff = None


    def test_get_ips_for_feature(self):
        """
        Make sure that hostnames in inventory are sorted.
        """

        with mock.patch('cli.engine.providers.any.APIProxy.Log', return_value='mock_Log') as mock_Log:
            proxy = APIProxy(CLUSTER_MODEL('any'), CONFIG_DOC())

            EXPECTED_RESULT = [
                AnsibleOrderedHostModel('service-vm-0', '20.73.105.240'),
                AnsibleOrderedHostModel('service-vm-1', '20.73.105.188'),
                AnsibleOrderedHostModel('service-vm-2', '20.73.105.18'),
                AnsibleOrderedHostModel('service-vm-3', '20.73.105.33'),
                AnsibleOrderedHostModel('service-vm-4', '20.73.105.54')
            ]

            result = proxy.get_ips_for_feature('service')

            self.assertListEqual(EXPECTED_RESULT, result)
