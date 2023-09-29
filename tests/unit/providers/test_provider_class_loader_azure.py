from cli.src.providers.azure.APIProxy import APIProxy
from cli.src.providers.azure.InfrastructureBuilder import InfrastructureBuilder
from cli.src.providers.provider_class_loader import provider_class_loader


def test_provider_class_loader_infrastructurebuilder_azure():
    infrastructure_builder = provider_class_loader('azure', 'InfrastructureBuilder')
    assert infrastructure_builder is InfrastructureBuilder


def test_provider_class_loader_apiproxy_azure():
    api_proxy = provider_class_loader('azure', 'APIProxy')
    assert api_proxy is APIProxy
