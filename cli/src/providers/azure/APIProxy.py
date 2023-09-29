import json
import re
import time
import os
from subprocess import PIPE, Popen

from cli.src.helpers.build_io import SP_FILE_NAME, get_terraform_path
from cli.src.helpers.data_loader import load_yaml_file
from cli.src.helpers.doc_list_helpers import select_first
from cli.src.helpers.naming_helpers import cluster_tag, resource_name
from cli.src.Log import Log, LogPipe
from cli.src.models.AnsibleHostModel import AnsibleOrderedHostModel


class APIProxy:
    def __init__(self, cluster_model, config_docs=[]):
        self.cluster_model = cluster_model
        self.cluster_name = self.cluster_model.specification.name.lower()
        self.cluster_prefix = None
        self.resource_group_name = resource_name(self.cluster_prefix, self.cluster_name, 'rg')
        self.config_docs = config_docs
        self.logger = Log(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def login_account(self):
        subscription_name = self.cluster_model.specification.cloud.subscription_name
        tenant_id = self.cluster_model.specification.cloud.azure_login.tenant_id
        use_device_code = self.cluster_model.specification.cloud.azure_login.use_device_code
        login_command = f'az login --tenant {tenant_id}'
        if use_device_code:
            login_command = ' '.join([login_command, '--use-device-code'])
        all_subscription = self.run(self, login_command)
        subscription = select_first(all_subscription, lambda x: x['name'] == subscription_name)
        if subscription is None:
            raise Exception(f'User does not have access to subscription: "{subscription_name}"')
        return subscription

    def login_sp(self, sp_data):
        appId = sp_data['appId']
        password = sp_data['password']
        tenant = sp_data['tenant']
        return self.run(self, f'az login --service-principal -u \'{appId}\' -p \'{password}\' --tenant \'{tenant}\'', False)

    def set_active_subscription(self, subscription_id):
        self.run(self, f'az account set --subscription {subscription_id}')

    def get_active_subscribtion(self):
        subscription = self.run(self, 'az account show')
        return subscription

    def get_ips_for_feature(self, component_key):
        look_for_public_ip = self.cluster_model.specification.cloud.use_public_ips
        cluster = cluster_tag(self.cluster_prefix, self.cluster_name)
        running_instances = self.run(self, f'az vm list-ip-addresses --ids $(az resource list --query "[?type==\'Microsoft.Compute/virtualMachines\' && tags.{component_key} == \'\' && tags.cluster == \'{cluster}\'].id" --output tsv)')
        result: List[AnsibleOrderedHostModel] = []
        for instance in running_instances:
            if isinstance(instance, list):
                instance = instance[0]
            if self.cluster_model.specification.cloud.hostname_domain_extension != '':
                name = instance['virtualMachine']['name'] + f'.{self.cluster_model.specification.cloud.hostname_domain_extension}'
            else:
                name = instance['virtualMachine']['name']
            if look_for_public_ip:
                ip = instance['virtualMachine']['network']['publicIpAddresses'][0]['ipAddress']
            else:
                ip = instance['virtualMachine']['network']['privateIpAddresses'][0]
            result.append(AnsibleOrderedHostModel(name, ip))

        result.sort()

        return result

    def login(self, env=None):
        # https://learn.microsoft.com/en-us/azure/developer/terraform/authenticate-to-azure
        # We support:
        # - Authenticating to Azure using the Azure CLI
        # - Authenticating to Azure using a Service Principal and a Client Secret
        if not self.cluster_model.specification.cloud.use_service_principal:
            # Account
            subscription = self.login_account()
            self.set_active_subscription(subscription['id'])
        else:
            # Service principal
            sp_file = os.path.join(get_terraform_path(self.cluster_model.specification.name), SP_FILE_NAME)
            if os.path.exists(sp_file):
                self.logger.info('Using service principal from sp.yml file')
                sp = load_yaml_file(sp_file)
            elif hasattr(self.cluster_model.specification.cloud, 'service_principal'):
                self.logger.info('Using service principal from cloud section in the cluster configuration file')
                sp = self.cluster_model.specification.cloud.service_principal
            else:
                raise Exception(f'No service principal defined in the cloud section of the cluster configuration file or in an sp.yml file.')

            # Login as SP and get the default subscription.
            subscription = self.login_sp(sp)

            if 'subscriptionId' in sp:
                # Set active subscription if sp contains it.
                self.set_active_subscription(sp['subscriptionId'])
                env['ARM_SUBSCRIPTION_ID'] = sp['subscriptionId']
            else:
                # No subscriptionId in sp.yml so use the default one from Azure SP login.
                env['ARM_SUBSCRIPTION_ID'] = subscription[0]['id']

            # Set other environment variables for Terraform when working with Azure and service principal.
            env['ARM_TENANT_ID'] = sp['tenant']
            env['ARM_CLIENT_ID'] = sp['appId']
            env['ARM_CLIENT_SECRET'] = sp['password']

    def get_storage_account_primary_key(self, storage_account_name):
        keys = self.run(self, f'az storage account keys list -g \'{self.resource_group_name}\' -n \'{storage_account_name}\'')
        return keys[0]['value']

    @staticmethod
    def wait(self, seconds):
        for x in range(0, seconds):
            self.logger.info(f'Waiting {seconds} seconds...{x}')
            time.sleep(1)

    @staticmethod
    def run(self, cmd, log_cmd=True):
        if log_cmd:
            self.logger.info('Running: "' + cmd + '"')

        logpipe = LogPipe(__name__)
        with Popen(cmd, stdout=PIPE, stderr=logpipe, shell=True) as sp:
            logpipe.close()
            try:
                data = sp.stdout.read().decode('utf-8')
                data = re.sub(r'\s+', '', data)
                data = re.sub(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', '', data)
                output = json.loads(data)
            except:
                output = {}

        if sp.returncode != 0:
            if log_cmd:
                raise Exception(f'Error running: "{cmd}"')
            else:
                raise Exception('Error running Azure APIProxy cmd')
        else:
            if log_cmd:
                self.logger.info(f'Done running "{cmd}"')
            return output
