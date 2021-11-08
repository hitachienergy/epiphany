from typing import List

from cli.models.AnsibleHostModel import AnsibleOrderedHostModel


def test_sort():
    """
    Test the `less` operator
    """

    EXPECTED_HOSTS: List[AnsibleOrderedHostModel] = [
        AnsibleOrderedHostModel('prefix-cluster-service-vm-0', '20.82.14.10'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-1', '20.82.14.34'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-2', '20.82.14.101'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-3', '20.82.14.67'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-4', '20.82.14.11'),
    ]

    unordered_hosts: List[AnsibleOrderedHostModel] = [
        AnsibleOrderedHostModel('prefix-cluster-service-vm-4', '20.82.14.11'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-1', '20.82.14.34'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-3', '20.82.14.67'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-0', '20.82.14.10'),
        AnsibleOrderedHostModel('prefix-cluster-service-vm-2', '20.82.14.101')
    ]

    unordered_hosts.sort()

    assert EXPECTED_HOSTS == unordered_hosts
