#!/usr/bin/env py
import sys
import argparse
import json
import os

from cli.engine.BuildEngine import BuildEngine
from cli.engine.PatchEngine import PatchEngine
from cli.engine.DeleteEngine import DeleteEngine
from cli.engine.InitEngine import InitEngine
from cli.helpers.Log import Log
from cli.helpers.Config import Config
from cli.version import VERSION
from cli.licenses import LICENSES
from cli.helpers.query_yes_no import query_yes_no


def main():

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
    parser.add_argument('--log_type', choices=['plain', 'json'], default='plain',
                        dest='log_type', action='store', help='Type of logs.')
    parser.add_argument('--validate_certs', choices=['true', 'false'], default='true', action='store', dest='validate_certs',
                        help='''[Experimental]: Disables certificate checks for certain Ansible operations
                         which might have issues behind proxies (https://github.com/ansible/ansible/issues/32750). 
                         Should NOT be used in production for security reasons.''')
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
    delete_parser(subparsers)

    # check if there were any variables and display full help
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    arguments = sys.argv[1:]

    # add some arguments to the general config so we can easily use them throughout the CLI
    args = parser.parse_args(arguments)

    config.output_dir = args.output_dir if hasattr(args, 'output_dir') else None
    config.log_file = args.log_name
    config.log_format = args.log_format
    config.log_date_format = args.log_date_format
    config.log_type = args.log_type
    config.log_count = args.log_count
    config.validate_certs = True if args.validate_certs == 'true' else False

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
    sub_parser.add_argument('-p', '--provider', dest='provider', choices=['aws', 'azure', 'any'], default='any', type=str,
                            required=True, help='One of the supported providers: azure|aws|any')
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


def delete_parser(subparsers):
    sub_parser = subparsers.add_parser('recovery', description='[Experimental]: Recover from existing backup.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')
    sub_parser.set_defaults(func=run_recovery)


def recovery_parser(subparsers):
    sub_parser = subparsers.add_parser('delete', description='[Experimental]: Delete a cluster from build artifacts.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')
    sub_parser.set_defaults(func=run_delete)


def run_apply(args):
    adjust_paths_from_file(args)
    with BuildEngine(args) as engine:
        return engine.apply()


def run_validate(args):
    adjust_paths_from_file(args)
    with BuildEngine(args) as engine:
        return engine.verify()


def run_init(args):
    Config().output_dir = os.getcwd()
    with InitEngine(args) as engine:
        return engine.init()


def run_upgrade(args):
    if not query_yes_no('This is an experimental feature and could change at any time. Do you want to continue?'):
        return 0
    Config().output_dir = args.build_directory
    with PatchEngine() as engine:
        return engine.upgrade()


def run_backup(args):
    if not query_yes_no('This is an experimental feature and could change at any time. Do you want to continue?'):
        return 0
    Config().output_dir = args.build_directory
    with PatchEngine() as engine:
        return engine.backup()


def run_recovery(args):
    if not query_yes_no('This is an experimental feature and could change at any time. Do you want to continue?'):
        return 0
    Config().output_dir = args.build_directory
    with PatchEngine() as engine:
        return engine.recovery()


def run_delete(args):
    if not query_yes_no('This is an experimental feature and could change at any time. Do you want to continue?'):
        return 0
    if not query_yes_no('Do you really want to delete your cluster?'):
        return 0
    adjust_paths_from_build(args)
    with DeleteEngine(args) as engine:
        return engine.run()        


def adjust_paths_from_file(args):
    if not os.path.isabs(args.file):
        args.file = os.path.join(os.getcwd(), args.file)
    if not os.path.isfile(args.file):
        raise Exception(f'File "{args.file}" does not excist')        
    if Config().output_dir is None:
        Config().output_dir = os.path.join(os.path.dirname(args.file), 'build')
    dump_config(Config())


def adjust_paths_from_build(args):
    if not os.path.isabs(args.build_directory):
        args.build_directory = os.path.join(os.getcwd(), args.build_directory)
    if not os.path.exists(args.build_directory):
        raise Exception(f'Build directory "{args.build_directory}" does not excist')  
    if args.build_directory[-1:] == '/':    
        args.build_directory = args.build_directory.rstrip('/')
    if Config().output_dir is None:
        Config().output_dir = os.path.split(args.build_directory)[0]
    dump_config(Config())


def dump_config(config):
    logger = Log('config')
    for attr in config.__dict__:
        if attr.startswith('_'):
            logger.info ('%s = %r' % (attr[1:], getattr(config, attr)))


if __name__ == '__main__':
    exit(main())
