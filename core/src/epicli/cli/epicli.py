#!/usr/bin/env py
import sys
import argparse
from cli.helpers.Log import Log
from cli.helpers.Config import Config
from cli.engine.EpiphanyEngine import EpiphanyEngine
from cli.engine.version import VERSION


def main():
    arguments = [] if len(sys.argv) < 2 else sys.argv[1:]
    config = Config()
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage='''epicli <command> [<args>]''',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # setup some root arguments
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('-l', '--log_file', dest='log_name', type=str,
                        help='The name of the log file written to the output directory')
    parser.add_argument('-lf', '--log_format', dest='log_format', type=str,
                        help='Format for the logging string.')
    parser.add_argument('-ldf', '--log_date_format', dest='log_date_format', type=str,
                        help='Format for the logging date.')
    parser.add_argument('-lc', '--log_count', dest='log_count', type=str,
                        help='Roleover count where each CLI run will generate a new log.')
    # some arguments we don't want available when running from the docker image.
    if not config.docker_cli:
        parser.add_argument('-o', '--output', dest='output_dir', type=str,
                            help='Directory where the CLI should write it`s output.')

    # setup apply parser
    subparsers = parser.add_subparsers()
    apply_parser(subparsers)

    # add some arguments to the general config so we can easily use them throughout the CLI
    args = parser.parse_args(arguments)
    config.output_dir = args.output_dir if hasattr(args, 'output_dir') else None
    config.log_file = args.log_name
    config.log_format = args.log_format
    config.log_date_format = args.log_date_format
    config.log_count = args.log_count
    dump_config(config)

    return args.func(args)


def apply_parser(subparsers):
    sub_parser = subparsers.add_parser('apply', description='Applies configuration from file.')
    sub_parser.add_argument('-f', '--file', dest='file', type=str,
                            help='File with infrastructure/configuration definitions to use.')
    sub_parser.set_defaults(func=exec_apply)


def exec_apply(args):
    with EpiphanyEngine(args) as engine:
        engine.run()


def dump_config(config):
    logger = Log('config')
    for attr in config.__dict__:
        if attr.startswith('_'):
             logger.debug('%s = %r' % (attr[1:], getattr(config, attr)))


if __name__ == '__main__':
    sys.exit(main())
