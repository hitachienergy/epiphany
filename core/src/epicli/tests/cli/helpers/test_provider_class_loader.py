from cli.helpers.provider_class_loader import provider_class_loader
from cli.engine.aws.InfrastructureBuilder import InfrastructureBuilder


def test_provider_class_loader():
    infrastructure_builder = provider_class_loader('aws', 'InfrastructureBuilder')
    assert infrastructure_builder is InfrastructureBuilder
