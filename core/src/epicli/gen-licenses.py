import subprocess
import json
import os
import urllib.request
import logging
from itertools import dropwhile, takewhile
from functools import reduce
from typing import Set, List, Dict
import pkg_resources


def _get_dependencies_from_pipfile() -> Set[str]:
    with open('Pipfile') as pip_file:
        start_gen = dropwhile(lambda x: x.strip() != '[packages]', pip_file)
        next(start_gen)
        interesting_gen = takewhile(lambda x: not (x.startswith('[') or x == "\n"), start_gen)
        return {interesting.split()[0] for interesting in interesting_gen}


def _get_package_dependencies(dependencies: List[Dict[str, str]]) -> Set[str]:
    return {dependency['key'] for dependency in dependencies}


def _get_recursive_dependencies_for(direct_dependencies: Set[str]) -> Set[str]:
    result = subprocess.run(
        ['pipenv', 'graph', '--json'], stdout=subprocess.PIPE)
    dependencies_dict = {
        k['package']['key']: k
        for k in json.loads(result.stdout)
    }
    universe = set(dependencies_dict)
    res = direct_dependencies
    set_to_check = direct_dependencies
    while set_to_check:
        deps = universe & reduce(
            lambda x, y: x | _get_package_dependencies(dependencies_dict[y]['dependencies']),
            set_to_check, set())
        set_to_check = deps - res
        res = res | deps
    return {dependencies_dict[r]['package']['package_name'] for r in res}


def get_pkg_data(pkgname: str) -> str:
    pkgs = pkg_resources.require(pkgname)
    pkg = pkgs[0]
    pkg_data = {}
    print('Processing package: ', pkgname)
    for line in pkg.get_metadata_lines('METADATA'):
        try:
            (key, value) = line.split(': ', 1)
        except:
            continue
        if key == 'Name':
            pkg_data['Name'] = value
        if key == 'Version':
            pkg_data['Version'] = value
        if key == 'Summary':
            pkg_data['Summary'] = value
        if key == 'Home-page':
            pkg_data['Home-page'] = value
        if key == 'Author':
            pkg_data['Author'] = value
        if key == 'License':
            pkg_data['License'] = value

    home = pkg_data['Home-page'].lower().rstrip('/')
    if 'github' in home:
        try:
            split = home.split('/')
            repo = split[len(split)-1]
            user = split[len(split)-2]
            license_data = json.loads(urllib.request.urlopen('https://api.github.com/repos/' + user + '/' + repo + '/license' ).read().decode())
            pkg_data['License'] = license_data['license']['name']
            pkg_data['License repo'] = urllib.request.urlopen(license_data['download_url']).read().decode()
            if license_data['license']['key'] != 'other':
                license_text = json.loads(urllib.request.urlopen(license_data['license']['url']).read().decode())
                pkg_data['License text'] = license_text['body']
        except:
            logging.warning('Failed to pull in Github license information for package: ', pkgname)
    return pkg_data


def _main() -> None:
    direct_dependencies = _get_dependencies_from_pipfile()
    all_deps = _get_recursive_dependencies_for(direct_dependencies)
    all_deps_data = []
    for dep in all_deps:
        all_deps_data.append(get_pkg_data(dep))

    licenses_content = """
# This is a generated file so don`t change this manually. 
# To re-generate run 'python gen-licenses.py' from the project root.

LICENSES = """ + json.dumps(all_deps_data, indent=4)

    path = os.path.join(os.path.dirname(__file__), 'cli/licenses.py')
    with open(path, 'w') as file:
        file.write(licenses_content)

if __name__ == '__main__':
    _main()