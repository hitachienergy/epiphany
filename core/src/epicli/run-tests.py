#!/usr/bin/env py
import sys
import argparse
import json
import os
import subprocess

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage='''test <command> [<args>]''',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers()
    python_parser(subparsers)
    spec_parser(subparsers)

    arg = parser.parse_args()
    return arg.func(arg)


def python_parser(subparsers):
    sub_parser = subparsers.add_parser('python', description='Runs the Epicli python unit tests')

    def run_python(args):
        subprocess.call('mkdir -p tests/cli/results/ && python -m pytest ./tests/ --junit-xml=tests/cli/results/result.xml | tee tests/cli/results/result.txt', shell=True)

    sub_parser.set_defaults(func=run_python)


def spec_parser(subparsers):
    sub_parser = subparsers.add_parser('spec', description='Runs the serverspec tests against an existing cluster')
    sub_parser.add_argument('-i', '--inventory', dest='inventory', type=str, required=True,
                            help='The location of the inventory file of the cluster')
    sub_parser.add_argument('-u', '--user', dest='user', type=str, required=True,
                            help='The admin user of the machines in the cluster')                            
    sub_parser.add_argument('-k', '--key', dest='key', type=str, required=True,
                            help='The SSH key for the machines in the cluster')  

    def run_spec(args):
        subprocess.call(f'cd tests/serverspec-cli && rake inventory="{args.inventory}" user={args.user} keypath="{args.key}" spec:all', shell=True)

    sub_parser.set_defaults(func=run_spec)


if __name__ == '__main__':
    exit(main())
