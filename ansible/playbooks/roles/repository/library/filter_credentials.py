#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

from pathlib import Path
from typing import Callable, Dict, List
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
    in_place:
        description: When set to True will modify existing manifest passed as `src`
        required: false
        type: bool
"""

EXAMPLES = r"""
# Pass in a manifest file without modifying the original file
- name: Filter out manifest file and set result to stdout
  filter_credentials:
    src: /some/where/manifest.yml

# Pass in a manifest file and modify it in place
- name: Filter out manifest file and replace the original file
  filter_credentials:
    src: /some/where/manifest.yml
    in_place: true

# Pass in a manifest file and save it to `dest` location
- name: Filter out manifest file and save it as a new file
  filter_credentials:
    src: /some/where/manifest.yml
    dest: /some/other/place/manifest.yml
"""


from ansible.module_utils.basic import AnsibleModule


def _filter_common(docs: List[Dict]):
    # remove admin user info from epiphany-cluster doc:
    del next(filter(lambda doc: doc['kind'] == 'epiphany-cluster', docs))['specification']['admin_user']


def _filter_aws(docs: List[Dict]):
    _filter_common(docs)

    # filter epiphany-cluster doc
    epiphany_cluster = next(filter(lambda doc: doc['kind'] == 'epiphany-cluster', docs))
    del epiphany_cluster['specification']['cloud']['credentials']


def _filter_azure(docs: List[Dict]):
    _filter_common(docs)

    # filter epiphany-cluster doc
    epiphany_cluster = next(filter(lambda doc: doc['kind'] == 'epiphany-cluster', docs))
    del epiphany_cluster['specification']['cloud']['subscription_name']


def _get_filtered_manifest(manifest_path: Path) -> str:
    """
    Load the manifest file and remove any sensitive data.

    :param manifest_path: manifest file which will be loaded
    :returns: filtered manifset
    """
    docs = yaml.safe_load_all(manifest_path.open())
    filtered_docs = [doc for doc in docs if doc['kind'] in ['epiphany-cluster',
                                                            'configuration/feature-mappings',
                                                            'configuration/image-registry']]

    FILTER_DATA: Dict[str, Callable] = {
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
        in_place=dict(type=bool, required=False, default=False)
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

    # initialize check mode
    if module.check_mode:
        module.exit_json(**result)

    input_manifest = Path(module.params['src'])
    manifest = _get_filtered_manifest(input_manifest)

    if module.params['in_place'] and module.params['dest']:
        module.fail_json(msg='Cannot use `in_place` and `dest` at the same time', **result)

    if not module.params['in_place'] and not module.params['dest']:  # to stdout
        result['manifest'] = manifest
    elif module.params['in_place']:  # overwrite existing manifest
        with input_manifest.open(mode='w', encoding='utf-8') as mhandler:
            mhandler.write(manifest)
    elif module.params['dest']:  # write to a new location
        with Path(module.params['dest']).open(mode='w', encoding='utf-8') as output_manifest:
            output_manifest.write(manifest)

    result['changed'] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
