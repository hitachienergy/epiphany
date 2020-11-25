import sys
import subprocess
import json
import os
import urllib.request
import logging
from itertools import dropwhile, takewhile
from functools import reduce
from typing import Set, List, Dict
import pkg_resources
import textwrap


def get_dependencies_from_requirements() -> Set[str]:
    req = []
    with open('.devcontainer/requirements.txt') as req_file:
        for line in req_file:
            req.append(line.split("==")[0])
    return req

def makeRequest(url, token):
    request = urllib.request.Request(url)
    request.add_header('Authorization', 'token %s' % token)
    return urllib.request.urlopen(request)

def get_pkg_data(pkgname: str, pat:str) -> str:
    print('Processing package: ', pkgname)
    try:
        pkgs = pkg_resources.require(pkgname)
    except:
        logging.warning('Failed to get license information for package: ' + pkgname)
        return None
    pkg = pkgs[0]
    pkg_data = {}
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
            license_url = 'https://api.github.com/repos/' + user + '/' + repo + '/license'
            license_data = json.loads(makeRequest(license_url, pat).read().decode())
            pkg_data['License'] = license_data['license']['name']
            pkg_data['License URL'] = license_url
            pkg_data['License repo'] = makeRequest(license_data['download_url'], pat).read().decode()
            if license_data['license']['key'] != 'other':
                license_text =  json.loads(makeRequest(license_data['license']['url'], pat).read().decode())
                pkg_data['License text'] = license_text['body']
        except:
            logging.warning('Failed to pull in Github license information for package: ' + pkgname)

    return pkg_data


def _main() -> None:
    pat = sys.argv[1]
    if pat == None:
        logging.critical('No Github personal access tokens passed as argument.' )
        return
    all_deps = get_dependencies_from_requirements()
    all_deps_data = []
    for dep in all_deps:
        data = get_pkg_data(dep, pat)
        if data != None:
            all_deps_data.append(data)

    # Write licenses 'cli/licenses.py'
    licenses_content = """\
    # This is a generated file so don`t change this manually. 
    # To re-generate run 'python gen-licenses.py' from the project root.

    LICENSES = """

    licenses_content = textwrap.dedent(licenses_content) + json.dumps(all_deps_data, indent=4)

    path = os.path.join(os.path.dirname(__file__), 'cli/licenses.py')
    with open(path, 'w') as file:
        file.write(licenses_content)

     # Write components table to be pasted into 'COMPONENTS.md' and dependencies.xml for BDS scan
    dependencies_listing_content = textwrap.dedent("""\
    | Component | Version | Repo/Website | License |
    | --------- | ------- | ------------ | ------- |
    """)

    dependencies_content = """\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <components xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">"""

    count = 1
    for dep in all_deps_data: 
        dep_name = dep['Name']
        dep_version = dep['Version']
        dep_website = dep['Home-page']
        dep_license = dep['License']

        if 'License URL' in dep:
            dep_license_url = dep['License URL']
            dep_line = f'| {dep_name} | {dep_version} | {dep_website} | [{dep_license}]({dep_license_url}) |\n'
        else:
            dep_line = f'| {dep_name} | {dep_version} | {dep_website} | {dep_license} |\n'
        dependencies_listing_content = dependencies_listing_content + dep_line

        dependencies_content = dependencies_content + f"""
        <component>
            <id>{count}</id>
            <name>{dep_name}</name>
            <version>{dep_version}</version>
            <license>{dep_license}</license>
            <url>{dep_website}</url>
            <source></source>
        </component>"""
        count=count+1

    path = os.path.join(os.path.dirname(__file__), 'DEPENDENCIES.md')
    with open(path, 'w') as file:
        file.write(dependencies_listing_content)

    dependencies_content = dependencies_content + """
    </components>
    """
    path = os.path.join(os.path.dirname(__file__), 'dependencies.xml')
    with open(path, 'w') as file:
        file.write(textwrap.dedent(dependencies_content))

if __name__ == '__main__':
    _main()