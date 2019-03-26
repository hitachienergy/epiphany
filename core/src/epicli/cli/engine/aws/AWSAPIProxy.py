import boto3
from cli.helpers.list_helpers import select_single
from cli.helpers.objdict_helpers import dict_to_objdict
from cli.models.AnsibleHostModel import AnsibleHostModel


class AWSAPIProxy:
    def __init__(self, cluster_model, config_docs):
        self.cluster_model = cluster_model
        self.config_docs = config_docs

    def __enter__(self):
        credentials = self.cluster_model.specification.cloud.credentials
        self.client = boto3.client('ec2', aws_access_key_id=credentials.key, aws_secret_access_key=credentials.secret)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


    # Query AWS API for ec2 instances in state 'running' which are in cluster's VPC
    # and tagged with feature name (e.g. kubernetes_master) and cluster name
    def get_ips_for_feature(self, feature_key, look_for_public_ip=False):
        region = self.cluster_model.specification.cloud.region
        cluster_name = self.cluster_model.specification.name.lower()

        vpc_id = self.get_vpc_id()

        ec2 = boto3.resource('ec2', region)
        running_instances = ec2.instances.filter(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': ['running']
            },
            {
                'Name': 'vpc-id',
                'Values': [vpc_id]
            },
                {
                    'Name': 'tag:'+feature_key,
                    'Values': ['']
                },
                {
                    'Name': 'tag:cluster_name',
                    'Values': [cluster_name]
                }]
        )

        result = list()
        for instance in running_instances:
            if look_for_public_ip:
                result.append(AnsibleHostModel(instance.public_dns_name, instance.public_ip_address))
            else:
                result.append(AnsibleHostModel(instance.private_dns_name, instance.private_ip_address))
        return result

    def get_image_id(self, os_full_name):
        region = self.cluster_model.specification.cloud.region

        ec2 = boto3.resource('ec2', region)
        filters = [{
                'Name': 'name',
                'Values': [os_full_name]
            }]
        images = list(ec2.images.filter(Filters=filters))

        if len(images) == 1:
            return images[0].id

        raise Exception("Expected 1 OS Image matching Name: "+os_full_name+" but received: "+str(len(images)))

    def get_vpc_id(self):
        vpc_config = dict_to_objdict(select_single(self.config_docs, lambda x: x.kind == 'infrastructure/vpc'))
        region = self.cluster_model.specification.cloud.region
        ec2 = boto3.resource('ec2', region)
        filters = [{'Name': 'tag:Name', 'Values': [vpc_config.specification.name]}]
        vpcs = list(ec2.vpcs.filter(Filters=filters))

        if len(vpcs) == 1:
            return vpcs[0].id

        raise Exception("Expected 1 VPC matching tag Name: "+vpc_config.specification.name+" but received: "+str(len(vpcs)))

