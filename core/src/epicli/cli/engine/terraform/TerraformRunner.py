import os
from cli.engine.terraform.TerraformCommand import TerraformCommand
from cli.engine.providers.azure.APIProxy import APIProxy
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_terraform_path, save_sp, SP_FILE_NAME
from cli.helpers.data_loader import load_yaml_file


class TerraformRunner(Step):

    def __init__(self, cluster_model, config_docs):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.terraform = TerraformCommand(get_terraform_path(self.cluster_model.specification.name))

    def __enter__(self):
        super().__enter__()
        return self

    def run(self):
        pass

    def build(self):
        new_env = os.environ.copy()
        self.terraform.init(env=new_env)
        if self.cluster_model.provider == 'azure':
            self.azure_login()
        self.terraform.apply(auto_approve=True, env=new_env)

    def delete(self):
        new_env = os.environ.copy()
        if self.cluster_model.provider == 'azure':
            self.azure_login()
        self.terraform.destroy(auto_approve=True, env=new_env)
        
    def azure_login(self):
        # From the 4 methods terraform provides to login to 
        # Azure we support (https://www.terraform.io/docs/providers/azurerm/auth/azure_cli.html):
        # - Authenticating to Azure using the Azure CLI
        # - Authenticating to Azure using a Service Principal and a Client Secret
        apiproxy = APIProxy(self.cluster_model, self.config_docs)
        subscription = apiproxy.login()
        apiproxy.set_active_subscribtion(subscription['id'])

        if self.cluster_model.specification.cloud.use_service_principal:
            sp_file = os.path.join(get_terraform_path(self.cluster_model.specification.name), SP_FILE_NAME)
            if not os.path.exists(sp_file):
                self.logger.info('Creating service principal')
                sp = apiproxy.create_sp(self.cluster_model.specification.cloud.resource_group_name, subscription['id'])
                save_sp(sp, self.cluster_model.specification.name)
            else:
                self.logger.info('Using service principal from file')
                sp = load_yaml_file(sp_file)

            #Setup environment variables for Terraform when working with Azure and service principal.
            new_env['ARM_SUBSCRIPTION_ID'] = subscription['id']
            new_env['ARM_TENANT_ID'] = sp['tenant']
            new_env['ARM_CLIENT_ID'] = sp['appId']
            new_env['ARM_CLIENT_SECRET'] = sp['password']
