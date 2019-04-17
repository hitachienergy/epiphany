#!/usr/local/bin -S pipenv run python
import sys
import argparse
from cli.helpers.Log import Log
from cli.helpers.Config import Config
from cli.engine.EpiphanyEngine import EpiphanyEngine


def main(arguments):
    config = Config()
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage='''epicli <command> [<args>]''',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # setup root arguments
    parser.add_argument('-l', '--log', dest='log_name', type=str,
                        help='The name of the log file written to the output directory')
    # some arguments we don't want available when running from the docker image.
    if not config.docker_cli:
        parser.add_argument('-o', '--output', dest='output_dir', type=str,
                            help='Directory where the CLI should write it`s output.')

    # setup apply parser
    subparsers = parser.add_subparsers()
    apply_parser(subparsers)

    # add some arguments to the general config so we can easily use them throughout the CLI
    args = parser.parse_args(arguments)
    config.output_dir = args.output_dir
    config.log_file = args.log_name
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
             logger.info('%s = %r' % (attr[1:], getattr(config, attr)))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
