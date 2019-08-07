import os
from cli.engine.TerraformCommand import TerraformCommand
from cli.engine.azure.AzureCommand import AzureCommand
from cli.helpers.Step import Step
from cli.helpers.build_saver import get_terraform_path, save_sp, SP_FILE_NAME
from cli.helpers.data_loader import load_yaml_file


class TerraformRunner(Step):

    def __init__(self, cluster_model):
        super().__init__(__name__)
        self.cluster_model = cluster_model
        self.terraform = TerraformCommand(get_terraform_path(self.cluster_model.specification.name))
        self.azure_cli = AzureCommand()

    def __enter__(self):
        super().__enter__()
        return self

    def run(self):
        new_env = os.environ.copy()

        #if the provider is Azure we need to login and setup service principle.
        if self.cluster_model.provider == 'azure':
            subscription_id = self.azure_cli.login(self.cluster_model.specification.cloud.subscription_name)
            sp_file = os.path.join(get_terraform_path(self.cluster_model.specification.name), SP_FILE_NAME)
            if not os.path.exists(sp_file):
                self.logger.info('Creating service principle')
                sp = self.azure_cli.create_sp(self.cluster_model.specification.cloud.resource_group_name, subscription_id)
                save_sp(sp, self.cluster_model.specification.name)
            else:
                self.logger.info('Using service principle from file')
                sp = load_yaml_file(sp_file)

            #Setup environment variables for Terraform when working with Azure.
            new_env['ARM_SUBSCRIPTION_ID'] = subscription_id
            new_env['ARM_CLIENT_ID'] = sp['appId']
            new_env['ARM_CLIENT_SECRET'] = sp['password']
            new_env['ARM_TENANT_ID'] = sp['tenant']

        self.terraform.init(env=new_env)
        self.terraform.apply(auto_approve=True, env=new_env)