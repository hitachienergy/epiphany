#!/usr/bin/env py
import sys
import argparse
import json
import os

from cli.engine.PatchEngine import PatchEngine
from cli.engine.UserConfigInitializer import UserConfigInitializer
from cli.helpers.Log import Log
from cli.helpers.Config import Config
from cli.engine.EpiphanyEngine import EpiphanyEngine
from cli.version import VERSION
from cli.licenses import LICENSES


def main():
    arguments = [] if len(sys.argv) < 2 else sys.argv[1:]
    config = Config()
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage='''epicli <command> [<args>]''',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # setup some root arguments
    parser.add_argument('--version', action='version', help='Shows the CLI version', version=VERSION)
    parser.add_argument('--licenses', action='version',
                        help='Shows the third party packages and their licenses the CLI is using.',
                        version=json.dumps(LICENSES, indent=4))
    parser.add_argument('-l', '--log_file', dest='log_name', type=str,
                        help='The name of the log file written to the output directory')
    parser.add_argument('--log_format', dest='log_format', type=str,
                        help='Format for the logging string.')
    parser.add_argument('--log_date_format', dest='log_date_format', type=str,
                        help='Format for the logging date.')
    parser.add_argument('--log_count', dest='log_count', type=str,
                        help='Roleover count where each CLI run will generate a new log.')
    # some arguments we don't want available when running from the docker image.
    if not config.docker_cli:
        parser.add_argument('-o', '--output', dest='output_dir', type=str,
                            help='Directory where the CLI should write it`s output.')

    # setup subparsers
    subparsers = parser.add_subparsers()
    apply_parser(subparsers)
    validate_parser(subparsers)
    init_parser(subparsers)
    upgrade_parser(subparsers)
    backup_parser(subparsers)
    recovery_parser(subparsers)

    # add some arguments to the general config so we can easily use them throughout the CLI
    args = parser.parse_args(arguments)
    config.output_dir = args.output_dir if hasattr(args, 'output_dir') else None
    config.log_file = args.log_name
    config.log_format = args.log_format
    config.log_date_format = args.log_date_format
    config.log_count = args.log_count

    return args.func(args)


def apply_parser(subparsers):
    sub_parser = subparsers.add_parser('apply', description='Applies configuration from file.')
    sub_parser.add_argument('-f', '--file', dest='file', type=str,
                            help='File with infrastructure/configuration definitions to use.')
    sub_parser.add_argument('--no-infra', dest='no_infra', action="store_true",
                            help='Skip infrastructure provisioning.')

    sub_parser.set_defaults(func=run_apply)


def validate_parser(subparsers):
    sub_parser = subparsers.add_parser('verify', description='Validates the configuration from file by executing a dry '
                                                             'run without changing the physical '
                                                             'infrastructure/configuration')
    sub_parser.add_argument('-f', '--file', dest='file', type=str,
                            help='File with infrastructure/configuration definitions to use.')
    sub_parser.set_defaults(func=run_validate)


def init_parser(subparsers):
    sub_parser = subparsers.add_parser('init', description='Creates configuration file in working directory.')
    sub_parser.add_argument('-p', '--provider', dest='provider', type=str, required=True,
                            help='One of the supported providers: azure|aws|any')
    sub_parser.add_argument('-n', '--name', dest='name', type=str, required=True,
                            help='Name of the cluster.')

    sub_parser.add_argument('--full', dest='full_config', action="store_true",
                            help='Use this flag if you want to create verbose configuration file.')
    sub_parser.set_defaults(func=run_init)


def upgrade_parser(subparsers):
    sub_parser = subparsers.add_parser('upgrade', description='[Experimental]: Upgrades existing Epiphany Platform to latest version.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')
    sub_parser.set_defaults(func=run_upgrade)


def backup_parser(subparsers):
    sub_parser = subparsers.add_parser('backup', description='[Experimental]: Backups existing Epiphany Platform components.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')
    sub_parser.set_defaults(func=run_backup)


def recovery_parser(subparsers):
    sub_parser = subparsers.add_parser('recovery', description='[Experimental]: Recover from existing backup.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')
    sub_parser.set_defaults(func=run_recovery)


def run_apply(args):
    adjust_paths(args)
    with EpiphanyEngine(args) as engine:
        engine.apply()


def run_validate(args):
    adjust_paths(args)
    with EpiphanyEngine(args) as engine:
        engine.verify()


def run_init(args):
    Config().output_dir = os.getcwd()
    with UserConfigInitializer(args) as initializer:
        initializer.run()


def run_upgrade(args):
    Config().output_dir = args.build_directory
    with PatchEngine() as engine:
        engine.run_upgrade()


def run_backup(args):
    Config().output_dir = args.build_directory
    with PatchEngine() as engine:
        engine.run_backup()


def run_recovery(args):
    Config().output_dir = args.build_directory
    with PatchEngine() as engine:
        engine.run_recovery()


def adjust_paths(args):
    args.file = get_config_file_path(args.file)
    adjust_output_dir(args.file)
    dump_config(Config())


def get_config_file_path(config_file_path):
    if os.path.isabs(config_file_path):
        return config_file_path
    return os.path.join(os.getcwd(), config_file_path)


def adjust_output_dir(config_file_path):
    if Config().output_dir is None:
        config_directory = os.path.dirname(config_file_path)
        Config().output_dir = os.path.join(config_directory, 'build')


def dump_config(config):
    logger = Log('config')
    for attr in config.__dict__:
        if attr.startswith('_'):
            logger.debug('%s = %r' % (attr[1:], getattr(config, attr)))


if __name__ == '__main__':
    exit(main())
