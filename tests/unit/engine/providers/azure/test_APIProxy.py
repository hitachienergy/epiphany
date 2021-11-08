from unittest import mock, TestCase

from cli.engine.providers.azure.APIProxy import APIProxy
from cli.models.AnsibleHostModel import AnsibleOrderedHostModel
from tests.unit.engine.providers.data.APIProxy_data import CLUSTER_MODEL, RUNNING_INSTANCES_AZURE


class APIProxyTest(TestCase):
    """ Tests for `azure` provider """

    def setUp(self):
        self.maxDiff = None

    def test_get_ips_for_feature(self):
        """
        Make sure that hostnames in inventory are sorted.
        """

        with mock.patch('cli.engine.providers.azure.APIProxy.Log', return_value='mock_Log') as mock_Log:
            proxy = APIProxy(CLUSTER_MODEL('azure'), RUNNING_INSTANCES_AZURE)
            proxy.run = (lambda *args: RUNNING_INSTANCES_AZURE)  # mock run with prepared data

            EXPECTED_RESULT = [
                AnsibleOrderedHostModel('prefix-cluster-service-vm-0', '20.73.105.240'),
                AnsibleOrderedHostModel('prefix-cluster-service-vm-1', '20.73.105.188'),
                AnsibleOrderedHostModel('prefix-cluster-service-vm-2', '20.73.105.18'),
                AnsibleOrderedHostModel('prefix-cluster-service-vm-3', '20.73.105.33'),
                AnsibleOrderedHostModel('prefix-cluster-service-vm-4', '20.73.105.54')
            ]

            result = proxy.get_ips_for_feature('service')

            self.assertListEqual(EXPECTED_RESULT, result)
