from typing import Dict, List

from cli.src.helpers.ObjDict import ObjDict
from cli.src.helpers.objdict_helpers import dict_to_objdict


def CONFIG_DOC() -> ObjDict:
    return dict_to_objdict([
        {
            'kind': 'infrastructure/machine',
            'title': 'Virtual Machine Infra',
            'provider': 'any',
            'name': 'service-0',
            'specification': {
                'ip': '20.73.105.18',
                'hostname': 'service-vm-2'
            },
            'version': '1.3.0dev'
        },
        {
            'kind': 'infrastructure/machine',
            'title': 'Virtual Machine Infra',
            'provider': 'any',
            'name': 'service-1',
            'specification': {
                'ip': '20.73.105.54',
                'hostname': 'service-vm-4'
            },
            'version': '1.3.0dev'
        },
        {
            'kind': 'infrastructure/machine',
            'title': 'Virtual Machine Infra',
            'provider': 'any',
            'name': 'service-2',
            'specification': {
                'ip': '20.73.105.188',
                'hostname': 'service-vm-1'
            },
            'version': '1.3.0dev'
        },
        {
            'kind': 'infrastructure/machine',
            'title': 'Virtual Machine Infra',
            'provider': 'any',
            'name': 'service-3',
            'specification': {
                'ip': '20.73.105.240',
                'hostname': 'service-vm-0'
            },
            'version': '1.3.0dev'
        },
        {
            'kind': 'infrastructure/machine',
            'title': 'Virtual Machine Infra',
            'provider': 'any',
            'name': 'service-4',
            'specification': {
                'ip': '20.73.105.33',
                'hostname': 'service-vm-3'
            },
            'version': '1.3.0dev'
        },
    ])


def CLUSTER_MODEL(provider: str) -> ObjDict:
    return dict_to_objdict({
        'kind': 'epiphany-cluster',
        'title': 'Epiphany cluster Config',
        'provider': f'{provider}',
        'name': 'default',
        'specification': {
            'prefix': 'prefix',
            'name': 'cluster',
            'admin_user': {
                'name': 'username',
                'key_path': '/path/to/key'
            },
            'cloud': {
                'k8s_as_cloud_service': False,
                'subscription_name': 'Subscription Name',
                'vnet_address_pool': '10.1.0.0/20',
                'use_public_ips': True,
                'use_service_principal': False,
                'region': 'West Europe',
                'network': {'use_network_security_groups': True},
                'default_os_image': 'default',
                'hostname_domain_extension': '',
                'credentials': {
                    'access_key_id': 'key',
                    'secret_access_key': 'secret',
                    'session_token': 'token'
                }
            },
            'components': {
                'service': {
                    'count': 5,
                    'machine': 'service-machine',
                    'configuration': 'default',
                    'subnets': [{'address_pool': '10.1.8.0/24'}],
                    'machines': ['service-0',
                                 'service-1',
                                 'service-2',
                                 'service-3',
                                 'service-4']
                }
            }
        },
        'version': '1.3.0dev'
    })

RUNNING_INSTANCES_AZURE: List[List[Dict]] = [
    [
        {'virtualMachine': {
            'name': 'prefix-cluster-service-vm-0',
            'network': {
                'privateIpAddresses': ['10.1.8.6'],
                'publicIpAddresses': [
                    {'id': '/subscriptions/subscription_hash/resourceGroups/prefix-cluster-rg/providers/Microsoft.Network/publicIPAddresses/prefix-cluster-service-pubip-0',
                     'ipAddress': '20.73.105.240',
                     'ipAllocationMethod': 'Static',
                     'name': 'prefix-cluster-service-pubip-0',
                     'resourceGroup': 'prefix-cluster-rg',
                     'zone': '1'}
                ]
            },
            'resourceGroup': 'prefix-cluster-rg'}
        }
    ],
    [
        {'virtualMachine': {
            'name': 'prefix-cluster-service-vm-2',
            'network': {
                'privateIpAddresses': ['10.1.8.5'],
                'publicIpAddresses': [
                    {'id': '/subscriptions/subscription_hash/resourceGroups/prefix-cluster-rg/providers/Microsoft.Network/publicIPAddresses/prefix-cluster-service-pubip-2',
                     'ipAddress': '20.73.105.18',
                     'ipAllocationMethod': 'Static',
                     'name': 'prefix-cluster-service-pubip-2',
                     'resourceGroup': 'prefix-cluster-rg',
                     'zone': '1'}
                ]
            },
            'resourceGroup': 'prefix-cluster-rg'}
        }
    ],
    [
        {'virtualMachine': {
            'name': 'prefix-cluster-service-vm-1',
            'network': {
                'privateIpAddresses': ['10.1.8.4'],
                'publicIpAddresses': [
                    {'id': '/subscriptions/subscription_hash/resourceGroups/prefix-cluster-rg/providers/Microsoft.Network/publicIPAddresses/prefix-cluster-service-pubip-2',
                     'ipAddress': '20.73.105.188',
                     'ipAllocationMethod': 'Static',
                     'name': 'prefix-cluster-service-pubip-1',
                     'resourceGroup': 'prefix-cluster-rg',
                     'zone': '1'}
                ]
            },
            'resourceGroup': 'prefix-cluster-rg'}
        }
    ],
    [
        {'virtualMachine': {
            'name': 'prefix-cluster-service-vm-4',
            'network': {
                'privateIpAddresses': ['10.1.8.3'],
                'publicIpAddresses': [
                    {'id': '/subscriptions/subscription_hash/resourceGroups/prefix-cluster-rg/providers/Microsoft.Network/publicIPAddresses/prefix-cluster-service-pubip-2',
                     'ipAddress': '20.73.105.54',
                     'ipAllocationMethod': 'Static',
                     'name': 'prefix-cluster-service-pubip-4',
                     'resourceGroup': 'prefix-cluster-rg',
                     'zone': '1'}
                ]
            },
            'resourceGroup': 'prefix-cluster-rg'}
        }
    ],
    [
        {'virtualMachine': {
            'name': 'prefix-cluster-service-vm-3',
            'network': {
                'privateIpAddresses': ['10.1.8.2'],
                'publicIpAddresses': [
                    {'id': '/subscriptions/subscription_hash/resourceGroups/prefix-cluster-rg/providers/Microsoft.Network/publicIPAddresses/prefix-cluster-service-pubip-2',
                     'ipAddress': '20.73.105.33',
                     'ipAllocationMethod': 'Static',
                     'name': 'prefix-cluster-service-pubip-3',
                     'resourceGroup': 'prefix-cluster-rg',
                     'zone': '1'}
                ]
            },
            'resourceGroup': 'prefix-cluster-rg'}
        }
    ]
]

class AWSMockInstance:
    def __init__(self, name, ip):
        self.tags = []
        self.tags.append({
            'Key': 'Name',
            'Value': name,
        })
        self.private_ip_address = ip
        self.public_ip_address = ip

RUNNING_INSTANCES_AWS: List[Dict] = [
    AWSMockInstance('prefix-cluster-service-vm-4', '20.73.105.54'),
    AWSMockInstance('prefix-cluster-service-vm-1', '20.73.105.188'),
    AWSMockInstance('prefix-cluster-service-vm-3', '20.73.105.33'),
    AWSMockInstance('prefix-cluster-service-vm-0', '20.73.105.240'),
    AWSMockInstance('prefix-cluster-service-vm-2', '20.73.105.18')
]
