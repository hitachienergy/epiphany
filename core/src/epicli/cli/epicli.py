#!/usr/bin/env py
import atexit
import sys
import argparse
import json
import os
import time
import json
import subprocess
import platform
import socket

from cli.engine.ApplyEngine import ApplyEngine
from cli.engine.BackupEngine import BackupEngine
from cli.engine.DeleteEngine import DeleteEngine
from cli.engine.InitEngine import InitEngine
from cli.engine.PrepareEngine import PrepareEngine
from cli.engine.RecoveryEngine import RecoveryEngine
from cli.engine.UpgradeEngine import UpgradeEngine
from cli.engine.TestEngine import TestEngine
from cli.helpers.Log import Log
from cli.helpers.Config import Config
from cli.version import VERSION
from cli.licenses import LICENSES
from cli.helpers.query_yes_no import query_yes_no
from cli.helpers.input_query import prompt_for_password
from cli.helpers.build_saver import save_to_file, get_output_path
from cli.engine.spec.SpecCommand import SpecCommand


def main():
    config = Config()
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage='''epicli <command> [<args>]''',
        formatter_class=argparse.RawTextHelpFormatter)

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
    parser.add_argument('--auto-approve', dest='auto_approve', action="store_true",
                        help='Auto approve any user input queries asked by Epicli')

    # set debug verbosity level.
    def debug_level(x):
        x = int(x)
        if x < 0 or x > 4:
            raise argparse.ArgumentTypeError("--debug value should be between 0 and 4")
        return x

    parser.add_argument('--debug', dest='debug', type=debug_level,
                        help='''Set this flag (0..4) to enable debug output where 0 is no
debug output and 1..4 is debug output with different verbosity levels:
Python    : Anything heigher then 0 enables printing of Python stacktraces
Ansible   : 1..4 map to following Ansible verbosity levels:
            1: -v
            2: -vv
            3: -vvv
            4: -vvvv
Terraform : 1..4 map to the following Terraform verbosity levels:
            1: WARN
            2: INFO
            3: DEBUG
            4: TRACE''')

    # some arguments we don't want available when running from the docker image.
    if not config.docker_cli:
        parser.add_argument('-o', '--output', dest='output_dir', type=str,
                            help='Directory where the CLI should write it`s output.')

    # setup subparsers
    subparsers = parser.add_subparsers()
    prepare_parser(subparsers)
    init_parser(subparsers)
    apply_parser(subparsers)
    upgrade_parser(subparsers)
    delete_parser(subparsers)
    test_parser(subparsers)
    '''
    validate_parser(subparsers)
    '''
    backup_parser(subparsers)
    recovery_parser(subparsers)

    # check if there were any variables and display full help
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    arguments = sys.argv[1:]

    # add some arguments to the general config so we can easily use them throughout the CLI
    args = parser.parse_args(arguments)

    config.output_dir = getattr(args, 'output_dir', None)
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
        logger.error(e, exc_info=(config.debug > 0))
        dump_debug_info()
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

        with InitEngine(args) as engine:
            return engine.init()

    sub_parser.set_defaults(func=run_init)


def prepare_parser(subparsers):
    sub_parser = subparsers.add_parser('prepare', description='Creates a folder with all prerequisites to setup the offline requirements to install a cluster offline.')
    sub_parser.add_argument('--os', type=str, required=True, dest='os', choices=['ubuntu-18.04', 'redhat-7', 'centos-7'],
                            help='The OS to prepare the offline requirements for: ubuntu-18.04|redhat-7|centos-7')

    def run_prepare(args):
        adjust_paths_from_output_dir()
        with PrepareEngine(args) as engine:
            return engine.prepare()

    sub_parser.set_defaults(func=run_prepare)       


def apply_parser(subparsers):
    sub_parser = subparsers.add_parser('apply', description='Applies configuration from file.')
    sub_parser.add_argument('-f', '--file', dest='file', type=str,
                            help='File with infrastructure/configuration definitions to use.')
    sub_parser.add_argument('--no-infra', dest='no_infra', action="store_true",
                            help='''Skip terraform infrastructure provisioning. 
                            Use this when you already have infrastructure available and only want to run the 
                            Ansible role provisioning.''')
    sub_parser.add_argument('--skip-config', dest='skip_config', action="store_true",
                            help='''Skip Ansible role provisioning.
                            Use this when you need to create cloud infrastructure and apply manual changes before
                            you want to run the Ansible role provisioning.''')                         
    sub_parser.add_argument('--offline-requirements', dest='offline_requirements', type=str,
                            help='Path to the folder with pre-prepared offline requirements.')    
    sub_parser.add_argument('--vault-password', dest='vault_password', type=str,
                            help='Password that will be used to encrypt build artifacts.')
    # developer options
    sub_parser.add_argument('--profile-ansible-tasks', dest='profile_ansible_tasks', action="store_true",
                            help='Enable Ansible profile_tasks plugin for timing tasks.')

    def run_apply(args):
        adjust_paths_from_file(args)
        ensure_vault_password_is_set(args)
        with ApplyEngine(args) as engine:
            return engine.apply()

    sub_parser.set_defaults(func=run_apply)


def delete_parser(subparsers):
    sub_parser = subparsers.add_parser('delete', description='Delete a cluster from build artifacts.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')

    def run_delete(args):
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
    # developer options
    sub_parser.add_argument('--profile-ansible-tasks', dest='profile_ansible_tasks', action="store_true",
                            help='Enable Ansible profile_tasks plugin for timing tasks.')

    def run_upgrade(args):
        adjust_paths_from_build(args)
        with UpgradeEngine(args) as engine:
            return engine.upgrade()

    sub_parser.set_defaults(func=run_upgrade)


def test_parser(subparsers):
    sub_parser = subparsers.add_parser('test', description='Test a cluster from build artifacts.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.')
    group_list = '{' + ', '.join(SpecCommand.get_spec_groups()) + '}'
    sub_parser.add_argument('-g', '--group', choices=SpecCommand.get_spec_groups(), default='all', action='store', dest='group', required=False, metavar=group_list,
                            help='Group of tests to be run, e.g. kafka.')

    def run_test(args):
        experimental_query()
        adjust_paths_from_build(args)
        with TestEngine(args) as engine:
            return engine.test()

    sub_parser.set_defaults(func=run_test)


'''
def validate_parser(subparsers):
    sub_parser = subparsers.add_parser('verify', description='Validates the configuration from file by executing a dry '
                                                             'run without changing the physical '
                                                             'infrastructure/configuration')
    sub_parser.add_argument('-f', '--file', dest='file', type=str,
                            help='File with infrastructure/configuration definitions to use.')

    def run_validate(args):
        adjust_paths_from_file(args)
        with ApplyEngine(args) as engine:
            return engine.validate()

    sub_parser.set_defaults(func=run_validate)    
'''


def backup_parser(subparsers):
    """Configure and execute backup of cluster components."""

    sub_parser = subparsers.add_parser('backup',
                                       description='Create backup of cluster components.')
    sub_parser.add_argument('-f', '--file', dest='file', type=str, required=True,
                            help='Backup configuration definition file to use.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.',
                            default=None)

    def run_backup(args):
        adjust_paths_from_file(args)
        with BackupEngine(args) as engine:
            return engine.backup()

    sub_parser.set_defaults(func=run_backup)


def recovery_parser(subparsers):
    """Configure and execute recovery of cluster components."""

    sub_parser = subparsers.add_parser('recovery',
                                       description='Recover from existing backup.')
    sub_parser.add_argument('-f', '--file', dest='file', type=str, required=True,
                            help='Recovery configuration definition file to use.')
    sub_parser.add_argument('-b', '--build', dest='build_directory', type=str, required=True,
                            help='Absolute path to directory with build artifacts.',
                            default=None)

    def run_recovery(args):
        if not query_yes_no('Do you really want to perform recovery?'):
            return 0
        adjust_paths_from_file(args)
        with RecoveryEngine(args) as engine:
            return engine.recovery()

    sub_parser.set_defaults(func=run_recovery)


def experimental_query():
    if not query_yes_no('This is an experimental feature and could change at any time. Do you want to continue?'):
        sys.exit(0)


def adjust_paths_from_output_dir():
    if not Config().output_dir:
        Config().output_dir = os.getcwd()  # Default to working dir so we can at least write logs.


def adjust_paths_from_file(args):
    if not os.path.isabs(args.file):
        args.file = os.path.join(os.getcwd(), args.file)
    if not os.path.isfile(args.file):
        Config().output_dir = os.getcwd()  # Default to working dir so we can at least write logs.
        raise Exception(f'File "{args.file}" does not exist')
    if Config().output_dir is None:
        Config().output_dir = os.path.join(os.path.dirname(args.file), 'build')


def adjust_paths_from_build(args):
    if not os.path.isabs(args.build_directory):
        args.build_directory = os.path.join(os.getcwd(), args.build_directory)
    if not os.path.exists(args.build_directory):
        Config().output_dir = os.getcwd()  # Default to working dir so we can at least write logs.
        raise Exception(f'Build directory "{args.build_directory}" does not exist')
    if args.build_directory[-1:] == '/':
        args.build_directory = args.build_directory.rstrip('/')
    if Config().output_dir is None:
        Config().output_dir = os.path.split(args.build_directory)[0]

def ensure_vault_password_is_set(args):
    vault_password = args.vault_password 
    if vault_password is None:
        vault_password = prompt_for_password("Provide password to encrypt vault: ")

    directory_path = os.path.dirname(Config().vault_password_location)
    os.makedirs(directory_path, exist_ok=True)
    save_to_file(Config().vault_password_location, vault_password)


def ensure_vault_password_is_cleaned():
    if os.path.exists(Config().vault_password_location):
        os.remove(Config().vault_password_location)


def exit_handler():
    ensure_vault_password_is_cleaned()


def dump_debug_info():
    def dump_external_debug_info(title, args):
        dump_file.write(f'\n\n*****{title}******\n')
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        out, err = p.communicate()
        lines = filter(lambda x: x.strip(), out.decode("utf-8").splitlines(keepends=True))
        dump_file.writelines(lines)

    try:
        logger = Log('dump_debug_info')
        config = Config()

        timestr = time.strftime("%Y%m%d-%H%M%S")
        dump_path = os.getcwd() + f'/epicli_error_{timestr}.dump'
        dump_file = open(dump_path, 'w') 

        dump_file.write('*****EPICLI VERSION******\n')
        dump_file.write(f'{VERSION}')

        dump_file.write('\n\n*****EPICLI ARGS******\n')
        dump_file.write(' '.join([*['epicli'], *sys.argv[1:]]))        

        dump_file.write('\n\n*****EPICLI CONFIG******\n')
        for attr in config.__dict__:
            if attr.startswith('_'):
                dump_file.write('%s = %r\n' % (attr[1:], getattr(config, attr)))

        dump_file.write('\n\n*****SYSTEM******\n')      
        system_data = {
            'platform':platform.system(),
            'release':platform.release(),
            'type': platform.uname().system,
            'arch': platform.uname().machine,
            'cpus': json.dumps(os.cpu_count()),
            'hostname': socket.gethostname()
        }
        dump_file.write(json.dumps(dict(system_data), indent=2))

        dump_file.write('\n\n*****ENVIROMENT VARS******\n')
        dump_file.write(json.dumps(dict(os.environ), indent=2))

        dump_file.write('\n\n*****PYTHON******\n')
        dump_file.write(f'python_version: {platform.python_version()}\n') 
        dump_file.write(f'python_build: {platform.python_build()}\n')  
        dump_file.write(f'python_revision: {platform.python_revision()}\n')
        dump_file.write(f'python_compiler: {platform.python_compiler()}\n')    
        dump_file.write(f'python_branch: {platform.python_branch()}\n')    
        dump_file.write(f'python_implementation: {platform.python_implementation()}\n')  

        dump_external_debug_info('ANSIBLE VERSION', ['ansible', '--version'])
        dump_external_debug_info('ANSIBLE CONFIG', ['ansible-config', 'dump'])
        dump_external_debug_info('ANSIBLE-VAULT VERSION', ['ansible-vault', '--version'])
        dump_external_debug_info('TERRAFORM VERSION', ['terraform', '--version'])
        dump_external_debug_info('SKOPEO VERSION', ['skopeo', '--version'])
        dump_external_debug_info('RUBY VERSION', ['ruby', '--version'])
        dump_external_debug_info('RUBY GEM VERSION', ['gem', '--version'])
        dump_external_debug_info('RUBY INSTALLED GEMS', ['gem', 'query', '--local'])

        dump_file.write('\n\n*****LOG******\n')
        log_path = os.path.join(get_output_path(), config.log_file)
        dump_file.writelines([l for l in open(log_path).readlines()]) 
    finally:
        dump_file.close()
        logger.info(f'Error dump has been written to: {dump_path}')
        logger.warning('This dump might contain sensitive information. Check before sharing.')

if __name__ == '__main__':
    atexit.register(exit_handler)
    exit(main())
