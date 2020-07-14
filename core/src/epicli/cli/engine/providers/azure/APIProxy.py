import json
import re
import time
from subprocess import Popen, PIPE
from cli.helpers.Log import LogPipe, Log
from cli.helpers.doc_list_helpers import select_first
from cli.helpers.naming_helpers import resource_name, cluster_tag
from cli.models.AnsibleHostModel import AnsibleHostModel

class APIProxy:
    def __init__(self, cluster_model, config_docs):
        self.cluster_model = cluster_model
        self.cluster_name = self.cluster_model.specification.name.lower()
        self.cluster_prefix = self.cluster_model.specification.prefix.lower()
        self.resource_group_name = resource_name(self.cluster_prefix, self.cluster_name, 'rg')        
        self.config_docs = config_docs
        self.logger = Log(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def login_account(self):
        subscription_name = self.cluster_model.specification.cloud.subscription_name
        all_subscription = self.run(self, 'az login')
        subscription = select_first(all_subscription, lambda x: x['name'] == subscription_name)
        if subscription is None:
            raise Exception(f'User does not have access to subscription: "{subscription_name}"')
        return subscription

    def login_sp(self, sp_data):
        name = sp_data['name']
        password = sp_data['password']
        tenant = sp_data['tenant']
        return self.run(self, f'az login --service-principal -u \'{name}\' -p \'{password}\' --tenant \'{tenant}\'', False)      

    def set_active_subscribtion(self, subscription_id):
        self.run(self, f'az account set --subscription {subscription_id}')  

    def get_active_subscribtion(self):
        subscription = self.run(self, f'az account show') 
        return subscription   
    
    def create_sp(self, app_name, subscription_id):
        #TODO: make role configurable?
        sp = self.run(self, f'az ad sp create-for-rbac -n \'{app_name}\' --role=\'Contributor\' --scopes=\'/subscriptions/{subscription_id}\'')
        # Sleep for a while. Sometimes the call returns before the rights of the SP are finished creating.
        self.wait(self, 60)
        return sp  

    def get_ips_for_feature(self, component_key):
        look_for_public_ip = self.cluster_model.specification.cloud.use_public_ips
        cluster = cluster_tag(self.cluster_prefix, self.cluster_name)
        running_instances = self.run(self, f'az vm list-ip-addresses --ids $(az resource list --query "[?type==\'Microsoft.Compute/virtualMachines\' && tags.{component_key} == \'\' && tags.cluster == \'{cluster}\'].id" --output tsv)')
        result = []
        for instance in running_instances:
            if isinstance(instance, list):
                instance = instance[0]   
            name = instance['virtualMachine']['name']
            if look_for_public_ip:
                ip = instance['virtualMachine']['network']['publicIpAddresses'][0]['ipAddress']
            else:
                ip = instance['virtualMachine']['network']['privateIpAddresses'][0]
            result.append(AnsibleHostModel(name, ip))
        return result

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
                raise Exception(f'Error running Azure APIProxy cmd')
        else:
            if log_cmd:
                self.logger.info(f'Done running "{cmd}"')
            return output            