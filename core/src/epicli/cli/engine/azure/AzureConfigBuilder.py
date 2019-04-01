from cli.engine.InfrastructureConfigBuilder import InfrastructureConfigBuilder


class AzureConfigBuilder(InfrastructureConfigBuilder):
    def build(self, cluster_model, user_input):
        raise NotImplementedError()

