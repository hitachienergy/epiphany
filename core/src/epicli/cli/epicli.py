#!/usr/bin/env py
import atexit
import sys
import argparse
import json
import os

from cli.engine.BuildEngine import BuildEngine
from cli.engine.PatchEngine import PatchEngine
from cli.engine.DeleteEngine import DeleteEngine
from cli.engine.InitEngine import InitEngine
from cli.engine.PrepareEngine import PrepareEngine
from cli.engine.UpgradeEngine import UpgradeEngine
from cli.helpers.Log import Log
from cli.helpers.Config import Config
from cli.version import VERSION
from cli.licenses import LICENSES
from cli.helpers.query_yes_no import query_yes_no
from cli.helpers.input_query import input_query
from cli.helpers.build_saver import save_to_file


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
    parser.add_argument('-l', '--log-file', dest='log_name', type=str,
                        help='The name of the log file written to the output directory')
    parser.add_argument('--log-format', dest='log_format', type=str,
                        help='Format for the logging string.')
    parser.add_argument('--log-date-format', dest='log_date_format', type=str,
                        help='Format for the logging date.')
    parser.add_argument('--log-count', dest='log_count', type=str,
                        help='Roleover count where each CLI run will generate a new log.')
    parser.add_argument('--log-type', choices=['plain', 'json'], default='plain',
                        dest='log_type', action='store', help='Type of logs.')
    parser.add_argument('--validate-certs', choices=['true', 'false'], default='true', action='store',
                        dest='validate_certs',
                        help='''[Experimental]: Disables certificate checks for certain Ansible operations
                         which might have issues behind proxies (https://github.com/ansible/ansible/issues/32750). 
                         Should NOT be used in production for security reasons.''')
    parser.add_argument('--debug', dest='debug', action="store_true",
                        help='Set this to output extensive debug information. Carries over to Ansible and Terraform.')
    parser.add_argument('--auto-approve', dest='auto_approve', action="store_true",
                        help='Auto approve any user input queries asked by Epicli')
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
    prepare_parser(subparsers)

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
    if 'offline_requirements' in args and not args.offline_requirements is None:
        config.offline_requirements = args.offline_requirements
    if 'wait_for_pods' in args and not args.wait_for_pods is None:
        config.wait_for_pods = args.wait_for_pods
    config.debug = args.debug
    config.auto_approve = args.auto_approve

    try:
        return args.func(args)
    except Exception as e:
        logger = Log('epicli')
        logger.error(e, exc_info=config.debug)
        return 1


def init_parser(subparsers):
    sub_parser = subparsers.add_parser('init', description='Creates configuration file in working directory.')
    sub_parser.add_argument('-p', '--provider', dest='provider', choices=['aws', 'azure', 'any'], default='any',
                            type=str,
                            required=True, help='One of the supported providers: azure|aws|any')
    sub_parser.add_argument('-n', '--name', dest='name', type=str, required=True,
                            help='Name of the cluster.')
    sub_parser.add_argument('--full', dest='full_config', action="store_true",
                            help='Use this flag if you want to create verbose configuration file.')

    def run_init(args):
        Config().output_dir = os.getcwd()
        dump_config(Config())
        with InitEngine(args) as engine:
            return engine.init()

    sub_parser.set_defaults(func=run_init)


def apply_parser(subparsers):
    sub_parser = subparsers.add_parser('apply', description='Applies configuration from file.')
    sub_parser.add_argument('-f', '--file', dest='file', type=str,
                            help='File with infrastructure/configuration definitions to use.')
    sub_parser.add_argument('--no-infra', dest='no_infra', action="store_true",
                            help='Skip infrastructure provisioning.')
    sub_parser.add_argument('--offline-requirements', dest='offline_requirements', type=str,
                            help='Path to the folder with pre-prepared offline requirements.')    
    sub_parser.add_argument('--vault-password', dest='vault_password', type=str,
                            help='Password that will be used to encrypt build artifacts.')

    def run_apply(args):
        adjust_paths_from_file(args)
        ensure_vault_password_is_set(args)
        with BuildEngine(args) as engine:
            return engine.apply()

    sub_parser.set_defaults(func=run_apply)


def validate_parser(subparsers):
    sub_parser = subparsers.add_parser('verify', description='Validates the configuration from file by executing a dry '
                                                             'run without changing the physical '
                                                             'infrastructure/configuration')
    sub_parser.add_argument('-f', '--file', dest='file', type=str,
                            help='File with infrastructure/configuration definitions to use.')

    def run_validate(args):
        adjust_paths_from_file(args)
        with BuildEngine(args) as engine:
            return engine.validate()

    sub_parser.set_defaults(func=run_validate)


def delete_parser(subparsers):
    sub_parser = subparsers.add_parser('delete', description='[Experimental]: Delete a cluster from build artifacts.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')

    def run_delete(args):
        experimental_query()
        if not query_yes_no('Do you really want to delete your cluster?'):
            return 0
        adjust_paths_from_build(args)
        with DeleteEngine(args) as engine:
            return engine.delete()

    sub_parser.set_defaults(func=run_delete)


def upgrade_parser(subparsers):
    sub_parser = subparsers.add_parser('upgrade',
                                       description='Upgrades common and K8s components of an existing Epiphany Platform cluster.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')
    sub_parser.add_argument('--wait-for-pods', dest='wait_for_pods', action="store_true",
                            help="Waits for all pods to be in the 'Ready' state before proceeding to the next step of the K8s upgrade.")
    sub_parser.add_argument('--offline-requirements', dest='offline_requirements', type=str, required=False,
                            help='Path to the folder with pre-prepared offline requirements.')

    def run_upgrade(args):
        adjust_paths_from_build(args)
        with UpgradeEngine(args) as engine:
            return engine.upgrade()

    sub_parser.set_defaults(func=run_upgrade)


def backup_parser(subparsers):
    sub_parser = subparsers.add_parser('backup',
                                       description='[Experimental]: Backups existing Epiphany Platform components.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')

    def run_backup(args):
        experimental_query()
        adjust_paths_from_build(args)
        with PatchEngine(args) as engine:
            return engine.backup()

    sub_parser.set_defaults(func=run_backup)


def recovery_parser(subparsers):
    sub_parser = subparsers.add_parser('recovery', description='[Experimental]: Recover from existing backup.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')

    def run_recovery(args):
        experimental_query()
        adjust_paths_from_build(args)
        with PatchEngine(args) as engine:
            return engine.recovery()

    sub_parser.set_defaults(func=run_recovery)


def prepare_parser(subparsers):
    sub_parser = subparsers.add_parser('prepare', description='Creates a folder with all prerequisites to setup the offline requirements to install a cluster offline.')
    sub_parser.add_argument('--os', type=str, required=True, dest='os',
                            help='The OS to prepare the offline requirements for.')

    def run_prepare(args):
        adjust_paths_from_output_dir()
        with PrepareEngine(args) as engine:
            return engine.prepare()

    sub_parser.set_defaults(func=run_prepare)   


def experimental_query():
    if not query_yes_no('This is an experimental feature and could change at any time. Do you want to continue?'):
        sys.exit(0)


def adjust_paths_from_output_dir():
    if not Config().output_dir:
        Config().output_dir = os.getcwd()  # Default to working dir so we can at least write logs.
    dump_config(Config())


def adjust_paths_from_file(args):
    if not os.path.isabs(args.file):
        args.file = os.path.join(os.getcwd(), args.file)
    if not os.path.isfile(args.file):
        Config().output_dir = os.getcwd()  # Default to working dir so we can at least write logs.
        raise Exception(f'File "{args.file}" does not excist')
    if Config().output_dir is None:
        Config().output_dir = os.path.join(os.path.dirname(args.file), 'build')
    dump_config(Config())


def adjust_paths_from_build(args):
    if not os.path.isabs(args.build_directory):
        args.build_directory = os.path.join(os.getcwd(), args.build_directory)
    if not os.path.exists(args.build_directory):
        Config().output_dir = os.getcwd()  # Default to working dir so we can at least write logs.
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
            logger.info('%s = %r' % (attr[1:], getattr(config, attr)))

def ensure_vault_password_is_set(args):
    vault_password = args.vault_password 
    if vault_password is None:
        vault_password = input_query("Provide password to encrypt vault")

    directory_path = os.path.dirname(Config().vault_password_location)
    os.makedirs(directory_path, exist_ok=True)
    save_to_file(Config().vault_password_location, vault_password)

def ensure_vault_password_cleaned():
    if os.path.exists(Config().vault_password_location):
        os.remove(Config().vault_password_location)

def exit_handler():
    ensure_vault_password_cleaned()

if __name__ == '__main__':
    atexit.register(exit_handler)
    exit(main())
