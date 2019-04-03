from cli.helpers.yaml_helpers import dump_all
import os

OUTPUT_FOLDER_PATH = '../../output/'
MANIFEST_FILE_NAME = 'manifest.yml'
INVENTORY_FILE_NAME = 'inventory'


def save_build(docs, cluster_name):
    script_dir = os.path.dirname(__file__)
    build_directory = os.path.join(script_dir, OUTPUT_FOLDER_PATH, cluster_name)
    if not os.path.exists(build_directory):
        os.makedirs(build_directory)
    with open(os.path.join(build_directory, MANIFEST_FILE_NAME), 'w') as stream:
        dump_all(docs, stream)


def save_inventory(inventory, cluster_name):
    script_dir = os.path.dirname(__file__)
    build_directory = os.path.join(script_dir, OUTPUT_FOLDER_PATH, cluster_name)
    if not os.path.exists(build_directory):
        os.makedirs(build_directory)
    with open(os.path.join(build_directory, INVENTORY_FILE_NAME), 'w') as file:
        for item in inventory:
            file.write('[' + item.role + ']\n')
            for host in item.hosts:
                file.write(host.name + ' ansible_host=' + host.ip + '\n')

