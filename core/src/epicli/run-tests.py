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

    arg = parser.parse_args()
    return arg.func(arg)


def python_parser(subparsers):
    sub_parser = subparsers.add_parser('python', description='Runs the Epicli python unit tests')

    def run_python(args):
        subprocess.call('mkdir -p tests/cli/results/ && python -m pytest ./tests/ --junit-xml=tests/cli/results/result.xml | tee tests/cli/results/result.txt', shell=True)

    sub_parser.set_defaults(func=run_python)


if __name__ == '__main__':
    exit(main())
