# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
del requirements[0]

datadir = os.path.join('data')
datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

print(requirements)

setup(
    name='epicli',
    version='0.3.0',
    description='Epiphany cli',
    long_description=readme,
    author='Epiphany Team',
    author_email='',
    url='https://github.com/epiphany-platform/epiphany',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    data_files=datafiles,
    entry_points={
        "console_scripts": [
            "epicli = cli.epicli:main"
        ]
    },
    install_requires=requirements
)
