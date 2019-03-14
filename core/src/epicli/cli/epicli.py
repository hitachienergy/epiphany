import sys
import argparse

from cli.engine.EpiphanyEngine import EpiphanyEngine


def exec_apply(args):
    with EpiphanyEngine(args) as engine:
        engine.run()


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage='''epicli <command> [<args>]''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers()
    # parser.add_argument('command', help='epicli command to run')
    # parser.add_argument('-f', '--environment', dest='environment', type=str, help='Environment to be used')
    # parser.add_argument('-t', '--template', dest='template', type=str, help='Template for data.yaml')
    # parser.add_argument('-id', '--identifier', dest='identifier', type=str, help='Example of str arg')
    # parser.add_argument('-i', '--infrastructure', action='store_true', help='Example of str arg')
    # args = parser.parse_args(sys.argv[1:2])
    apply_parser(subparsers)
    #parser.print_help()
    args = parser.parse_args(arguments)
    args.func(args)
    # todo return different return code if error


def apply_parser(subparsers):
    sub_parser = subparsers.add_parser('apply', description='Applies configuration from file.')
    sub_parser.add_argument('-c', '--context', dest='context', type=str, help='Epiphany cluster name that will be updated using this command')
    sub_parser.add_argument('-f', '--file', dest='file', type=str, help='File with infrastructure/configuration definitions to use.')
    sub_parser.set_defaults(func=exec_apply)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
