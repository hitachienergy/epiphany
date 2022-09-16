from cli.src.providers.any.APIProxy import APIProxy
from cli.src.providers.any.InfrastructureBuilder import InfrastructureBuilder
from cli.src.providers.provider_class_loader import provider_class_loader


def test_provider_class_loader_infrastructurebuilder_any():
    infrastructure_builder = provider_class_loader('any', 'InfrastructureBuilder')
    assert infrastructure_builder is InfrastructureBuilder


def test_provider_class_loader_apiproxy_any():
    api_proxy = provider_class_loader('any', 'APIProxy')
    assert api_proxy is APIProxy
