from abc import ABC, abstractmethod


class InfrastructureConfigBuilder(ABC):

    def __init__(self):
        super(InfrastructureConfigBuilder, self).__init__()

    @abstractmethod
    def build(self, model, component, component_name):
        pass
