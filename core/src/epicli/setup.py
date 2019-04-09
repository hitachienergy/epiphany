# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='epicli',
    version='0.3.0',
    description='Epiphany cli',
    long_description=readme,
    author='Epiphany Team',
    author_email='',
    url='https://github.com/epiphany-platform/epiphany',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
