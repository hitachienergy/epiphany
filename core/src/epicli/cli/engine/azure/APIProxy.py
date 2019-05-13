class APIProxy:
    def __init__(self, cluster_model, config_docs):
        self.cluster_model = cluster_model
        self.config_docs = config_docs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

