#!/usr/local/bin -S pipenv run python
import sys
import argparse

from cli.engine.EpiphanyEngine import EpiphanyEngine


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage='''epicli <command> [<args>]''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-o', '--output', dest='output', type=str, help='Directory where the CLI should write its output.')
    subparsers = parser.add_subparsers()
    apply_parser(subparsers)
    args = parser.parse_args(arguments)
    return args.func(args)


def apply_parser(subparsers):
    sub_parser = subparsers.add_parser('apply', description='Applies configuration from file.')
    sub_parser.add_argument('-f', '--file', dest='file', type=str, help='File with infrastructure/configuration definitions to use.')
    sub_parser.set_defaults(func=exec_apply)


def exec_apply(args):
    with EpiphanyEngine(args) as engine:
        engine.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
