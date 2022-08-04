#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

from hashlib import sha256
from pathlib import Path
from typing import Callable
import yaml

__metaclass__ = type


DOCUMENTATION = r"""
---
module: filter_credentials

short_description: Module for filtering sensitive data stored in manifest.yml file

options:
    src:
        description: Path to the manifest file that will be filtered
        required: true
        type: str
    dest:
        description: Path to the newly created, filtered manifest
        required: false
        type: str
"""

EXAMPLES = r"""
# Pass in a manifest file without modifying the original file
- name: Filter out manifest file and set result to stdout
  filter_credentials:
    src: /some/where/manifest.yml

# Pass in a manifest file and save it to `dest` location
- name: Filter out manifest file and save it as a new file
  filter_credentials:
    src: /some/where/manifest.yml
    dest: /some/other/place/manifest.yml
"""


from ansible.module_utils.basic import AnsibleModule


def _get_hash(filepath: Path) -> str:
    # calculate sha256 for `filepath`
    with filepath.open(mode='rb') as file_handler:
        hashgen = sha256()
        hashgen.update(file_handler.read())
        return hashgen.hexdigest()


def _filter_common(docs: list[dict]):
    # remove admin user info from epiphany-cluster doc:
    try:
        del next(filter(lambda doc: doc['kind'] == 'epiphany-cluster', docs))['specification']['admin_user']
    except KeyError:
        pass  # ok, key already doesn't exist


def _filter_aws(docs: list[dict]):
    _filter_common(docs)

    # filter epiphany-cluster doc
    epiphany_cluster = next(filter(lambda doc: doc['kind'] == 'epiphany-cluster', docs))

    try:
        del epiphany_cluster['specification']['cloud']['credentials']
    except KeyError:
        pass  # ok, key already doesn't exist


def _filter_azure(docs: list[dict]):
    _filter_common(docs)

    # filter epiphany-cluster doc
    epiphany_cluster = next(filter(lambda doc: doc['kind'] == 'epiphany-cluster', docs))
    try:
        del epiphany_cluster['specification']['cloud']['subscription_name']
    except KeyError:
        pass  # ok, key already doesn't exist


def _get_filtered_manifest(manifest_path: Path) -> str:
    """
    Load the manifest file and remove any sensitive data.

    :param manifest_path: manifest file which will be loaded
    :returns: filtered manifset
    """
    docs = yaml.safe_load_all(manifest_path.open())
    filtered_docs = [doc for doc in docs if doc['kind'] in ['epiphany-cluster',
                                                            'configuration/feature-mappings',
                                                            'configuration/features',
                                                            'configuration/image-registry']]

    FILTER_DATA: dict[str, Callable] = {
        'any': _filter_common,
        'azure': _filter_azure,
        'aws': _filter_aws
    }

    FILTER_DATA[filtered_docs[0]['provider']](filtered_docs)

    return yaml.dump_all(filtered_docs)

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        src=dict(type=str, required=True),
        dest=dict(type=str, required=False, default=None),
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
        manifest=''
    )

    # create ansible module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    input_manifest = Path(module.params['src'])
    output_manifest = Path(module.params['dest']) if module.params['dest'] else None

    manifest = _get_filtered_manifest(input_manifest)

    if not module.params['dest']:  # to stdout
        result['manifest'] = manifest
    else:  # write to a new location
        orig_hash_value = _get_hash(input_manifest)  # hash value prior to change

        with output_manifest.open(mode='w', encoding='utf-8') as output_manifest_file:
            output_manifest_file.write(manifest)

        new_hash_value = _get_hash(output_manifest)  # hash value post change

        if orig_hash_value != new_hash_value:
            result['changed'] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
