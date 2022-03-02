from cli.src.providers.aws.APIProxy import APIProxy
from cli.src.providers.aws.InfrastructureBuilder import InfrastructureBuilder
from cli.src.providers.aws.InfrastructureConfigCollector import \
    InfrastructureConfigCollector
from cli.src.providers.provider_class_loader import provider_class_loader


def test_provider_class_loader_infrastructurebuilder_aws():
    infrastructure_builder = provider_class_loader('aws', 'InfrastructureBuilder')
    assert infrastructure_builder is InfrastructureBuilder


def test_provider_class_loader_apiproxy_aws():
    api_proxy = provider_class_loader('aws', 'APIProxy')
    assert api_proxy is APIProxy


def test_provider_class_loader_infrastructureconfigcollector_aws():
    infrastructure_config_collector = provider_class_loader('aws', 'InfrastructureConfigCollector')
    assert infrastructure_config_collector is InfrastructureConfigCollector



