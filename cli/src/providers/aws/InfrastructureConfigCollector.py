from cli.src.helpers.doc_list_helpers import select_first, select_single
from cli.src.providers.aws.APIProxy import APIProxy
from cli.src.Step import Step


class InfrastructureConfigCollector(Step):

    def __init__(self, docs):
        super().__init__(__name__)
        self.cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
        self.docs = docs

    def run(self) -> dict:
        with APIProxy(self.cluster_model, self.docs) as proxy:
            return self.apply_efs_filesystem_id_for_k8s_pv(proxy)

    def apply_efs_filesystem_id_for_k8s_pv(self, proxy) -> dict:
        efs_storage_config = select_first(self.docs, lambda x: x.kind == 'infrastructure/efs-storage')
        kubernetes_config = select_first(self.docs, lambda x: x.kind == 'configuration/kubernetes-master')

        if self.should_apply_storage_settings(efs_storage_config, kubernetes_config):
            fs_id = proxy.get_efs_id_for_given_token(efs_storage_config.specification.token)
            kubernetes_config.specification.storage.data = {'server': self.get_efs_server_url(fs_id)}

        return kubernetes_config

    def should_apply_storage_settings(self, efs_storage_config, kubernetes_config):
        return efs_storage_config is not None and kubernetes_config is not None and \
               len(efs_storage_config.specification.mount_targets) > 0

    def get_efs_server_url(self, filesystem_id):
        return filesystem_id+'.efs.'+self.cluster_model.specification.cloud.region+'.amazonaws.com'
