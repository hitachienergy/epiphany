#!/usr/bin/env python

import json
import os
import sys
import argparse

import yaml
from jinja2 import Environment, FileSystemLoader


def merge_two_dicts(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Fill out manifest.yaml.j2 by accepting ips and data.yaml ('
                                            'workaround app)')

    p.add_argument('--data_file', '-d', help='data.yaml')
    p.add_argument('--azure_hosts', '-a', help='file with hosts')
    p.add_argument('--azure_storage_keys', '-k', help='azure storage keys')
    p.add_argument('--template_file', '-t', help='manifest.yaml.j2 file')
    p.add_argument('--output', '-o', help='output into')

    args = p.parse_args()

    with open(args.data_file, 'r') as data_file:
        data = yaml.load(data_file)

    with open(args.azure_hosts, 'r') as azure_hosts:
        hosts = yaml.load(azure_hosts)

    with open(args.azure_storage_keys, 'r') as azure_storage_keys:
        keys = yaml.load(azure_storage_keys)

    env = Environment(loader=FileSystemLoader('/'))
    env.filters['jsonify'] = json.dumps
    env.filters['to_nice_yaml'] = lambda x: yaml.safe_dump(x, default_flow_style=False)

    template = env.get_template(args.template_file)
    merged = merge_two_dicts(data, hosts)

    if 'k8s_storage_access_key' in keys and 'k8s_storage_account' in keys:
        merged['core']['kubernetes']['storage']['key'] = keys['k8s_storage_access_key']['value']
        merged['core']['kubernetes']['storage']['account'] = keys['k8s_storage_account']['value']

    with open(args.output, 'w') as f:
        rendered = template.render(merged)
        f.write(rendered)
