import json
import re
import time
from subprocess import Popen, PIPE
from cli.helpers.Log import LogPipe, Log
from cli.helpers.doc_list_helpers import select_first


class AzureCommand:
    def __init__(self):
        self.logger = Log(__name__)

    def login(self, subscription_name):
        all_subscription = self.run(self, 'az login')
        subscription = select_first(all_subscription, lambda x: x['name'] == subscription_name)
        if subscription is None:
            raise Exception(f'User does not have access to subscription: "{subscription_name}"')
        self.run(self, f'az account set --subscription {subscription["id"]}')
        return subscription['id']

    def create_sp(self, app_name, subscription_id):
        #TODO: make role configurable?
        sp = self.run(self, f'az ad sp create-for-rbac -n "{app_name}" --role="Contributor" --scopes="/subscriptions/{subscription_id}"')
        # Sleep for a while. Sometimes the call returns before the rights of the SP are finished creating.
        for x in range(0, 20):
            self.logger.info(f'Waiting 20 seconds...{x}')
            time.sleep(1)
        return sp

    @staticmethod
    def run(self, cmd):
        self.logger.info('Running: "' + cmd + '"')

        logpipe = LogPipe(__name__)
        with Popen(cmd, stdout=PIPE, stderr=logpipe, shell=True) as sp:
            logpipe.close()
            try:
                data = sp.stdout.read().decode("utf-8")
                data = re.sub(r'\s+', '', data)
                data = re.sub(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', '', data)
                output = json.loads(data)
            except:
                output = {}

        if sp.returncode != 0:
            raise Exception('Error running: "' + cmd + '"')
        else:
            self.logger.info('Done running "' + cmd + '"')
            return output
