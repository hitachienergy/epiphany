import os
from cli.engine.terraform.TerraformCommand import TerraformCommand
from cli.engine.providers.azure.APIProxy import APIProxy
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_terraform_path, save_sp, SP_FILE_NAME
from cli.helpers.data_loader import load_yaml_file
from cli.helpers.naming_helpers import resource_name

class TerraformRunner(Step):

    def __init__(self, cluster_model, config_docs):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.config_docs = config_docs
        self.terraform = TerraformCommand(get_terraform_path(self.cluster_model.specification.name))
        self.new_env = os.environ.copy()
        self.terraform.init(env=self.new_env)
        if self.cluster_model.provider == 'azure':
            self.azure_login()        

    def __enter__(self):
        super().__enter__()
        return self

    def run(self):
        pass

    def build(self):
        self.terraform.apply(auto_approve=True, env=self.new_env)

    def delete(self):
        self.terraform.destroy(auto_approve=True, env=self.new_env)
        
    def azure_login(self):
        # From the 4 methods terraform provides to login to 
        # Azure we support (https://www.terraform.io/docs/providers/azurerm/auth/azure_cli.html):
        # - Authenticating to Azure using the Azure CLI
        # - Authenticating to Azure using a Service Principal and a Client Secret
        apiproxy = APIProxy(self.cluster_model, self.config_docs)
        if not self.cluster_model.specification.cloud.use_service_principal:
            # Account
            subscription = apiproxy.login_account()
            apiproxy.set_active_subscribtion(subscription['id'])
        else:
            # Service principal
            sp_file = os.path.join(get_terraform_path(self.cluster_model.specification.name), SP_FILE_NAME)
            if not os.path.exists(sp_file):
                # If no service principal exists or is defined we created one and for that we need to login using an account
                subscription = apiproxy.login_account()
                apiproxy.set_active_subscribtion(subscription['id'])

                # Create the service principal, for now we use the default subscription
                self.logger.info('Creating service principal')
                cluster_name = self.cluster_model.specification.name.lower()
                cluster_prefix = self.cluster_model.specification.prefix.lower()               
                resource_group_name = resource_name(cluster_prefix, cluster_name, 'rg')
                sp = apiproxy.create_sp(resource_group_name, subscription['id'])
                sp['subscriptionId'] = subscription['id']
                save_sp(sp, self.cluster_model.specification.name)
            else:
                self.logger.info('Using service principal from file')
                sp = load_yaml_file(sp_file)

            # Login as SP and get the default subscription.
            subscription = apiproxy.login_sp(sp)

            if 'subscriptionId' in sp:
                # Set active subscription if sp contains it. 
                apiproxy.set_active_subscribtion(sp['subscriptionId'])
                self.new_env['ARM_SUBSCRIPTION_ID'] = sp['subscriptionId']
            else:
                # No subscriptionId in sp.yml so use the default one from Azure SP login.
                self.new_env['ARM_SUBSCRIPTION_ID'] = subscription[0]['id']

             # Set other environment variables for Terraform when working with Azure and service principal.
            self.new_env['ARM_TENANT_ID'] = sp['tenant']
            self.new_env['ARM_CLIENT_ID'] = sp['appId']
            self.new_env['ARM_CLIENT_SECRET'] = sp['password']
