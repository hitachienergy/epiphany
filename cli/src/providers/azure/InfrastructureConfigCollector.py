from cli.src.helpers.doc_list_helpers import select_first, select_single
from cli.src.providers.azure.APIProxy import APIProxy
from cli.src.Step import Step


class InfrastructureConfigCollector(Step):

    def __init__(self, docs):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.docs = docs

    def run(self) -> dict:
        with APIProxy(self.cluster_model, self.docs) as proxy:
            return self.apply_file_share_for_k8s_pv(proxy)

    def apply_file_share_for_k8s_pv(self, proxy) -> dict:
        storage_share_config = select_first(self.docs, lambda x: x.kind == 'infrastructure/storage-share')
        kubernetes_config = select_first(self.docs, lambda x: x.kind == 'configuration/kubernetes-master')

        if self.should_apply_storage_settings(storage_share_config, kubernetes_config):
            primary_key = proxy.get_storage_account_primary_key(storage_share_config.specification.storage_account_name)
            kubernetes_config.specification.storage.data = {
                'storage_account_name': storage_share_config.specification.storage_account_name,
                'storage_account_key': primary_key
            }

        return kubernetes_config

    def should_apply_storage_settings(self, storage_share_config, kubernetes_config):
        return storage_share_config is not None and kubernetes_config is not None
