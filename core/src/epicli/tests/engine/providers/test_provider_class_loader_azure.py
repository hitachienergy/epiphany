from cli.engine.providers.provider_class_loader import provider_class_loader
from cli.engine.providers.azure.InfrastructureBuilder import InfrastructureBuilder
from cli.engine.providers.azure.APIProxy import APIProxy
from cli.engine.providers.azure.InfrastructureConfigCollector import InfrastructureConfigCollector


def test_provider_class_loader_infrastructurebuilder_azure():
    infrastructure_builder = provider_class_loader('azure', 'InfrastructureBuilder')
    assert infrastructure_builder is InfrastructureBuilder


def test_provider_class_loader_apiproxy_azure():
    api_proxy = provider_class_loader('azure', 'APIProxy')
    assert api_proxy is APIProxy


def test_provider_class_loader_infrastructureconfigcollector_azure():
    infrastructure_config_collector = provider_class_loader('azure', 'InfrastructureConfigCollector')
    assert infrastructure_config_collector is InfrastructureConfigCollector



