from typing import Dict, List

from src.command.command import Command
from src.error import CriticalError


class DnfBase(Command):
    """
    Base class for `dnf` interfaces
    """

    def __init__(self, retries: int):
        super().__init__('dnf', retries)

    def _filter_non_critical_errors(self, stderr: str) -> str:
        output_lines = [line for line in stderr.split('\n')
                        if not line.startswith('Failed to set locale, defaulting to')]

        return '\n'.join(output_lines)


class Dnf(DnfBase):
    """
    Interface for `dnf`
    """

    def update(self, package: str = '',
                     disablerepo: str = '',
                     enablerepo: str = '',
                     ignore_already_installed_error: bool = False,
                     releasever: str = '',
                     assume_yes: bool = True):
        """
        Interface for `dnf update`

        :param package:
        :param disablerepo:
        :param enablerepo:
        :param ignore_already_installed_error: if set to True,
            `The same or higher version of {package} is already installed` error is ignored
        :param releasever:
        :param assume_yes: if set to True, -y flag will be used
        """
        update_parameters: List[str] = ['update']

        if assume_yes:
            update_parameters.append('-y')

        if package:
            update_parameters.append(package)

        if disablerepo:
            update_parameters.append(f'--disablerepo={disablerepo}')

        if enablerepo:
            update_parameters.append(f'--enablerepo={enablerepo}')

        if releasever:
            update_parameters.append(f'--releasever={releasever}')

        proc = self.run(update_parameters)

        if 'error' in proc.stdout:
            raise CriticalError(
                f'Found an error. dnf update failed for package `{package}`, reason: `{proc.stdout}`')

        filtered_stderr: str = self._filter_non_critical_errors(proc.stderr)

        if filtered_stderr:
            if (ignore_already_installed_error
                    and all(string in filtered_stderr for string in
                            ('The same or higher version', 'is already installed, cannot update it.'))):
                return

            raise CriticalError(
                f'dnf update failed for packages `{package}`, reason: `{proc.stderr}`')

    def install(self, package: str,
                assume_yes: bool = True,
                ignore_already_installed_error: bool = False):
        """
        Interface for `dnf install -y`

        :param package: packaged to be installed
        :param assume_yes: if set to True, -y flag will be used
        :param ignore_already_installed_error: if set to True,
            `The same or higher version of {package} is already installed` error is ignored
        """
        no_ask: str = '-y' if assume_yes else ''
        proc = self.run(['install', no_ask, package], accept_nonzero_returncode=True)

        if proc.returncode != 0:
            if 'does not update' not in proc.stdout:  # trying to reinstall package with url
                raise CriticalError(f'dnf install failed for `{package}`, reason `{proc.stdout}`')

        if 'error' in proc.stdout:
            raise CriticalError(
                f'Found an error. dnf install failed for package `{package}`, reason: `{proc.stdout}`')
        if self._filter_non_critical_errors(proc.stderr):
            if ignore_already_installed_error:
                if any('is already installed' in line for line in proc.stdout.split('\n')):
                    return

            raise CriticalError(f'dnf install failed for package `{package}`, reason: `{proc.stderr}`')

    def remove(self, package: str,
               assume_yes: bool = True):
        """
        Interface for `dnf remove -y`

        :param package: packaged to be removed
        :param assume_yes: if set to True, -y flag will be used
        """
        no_ask: str = '-y' if assume_yes else ''
        self.run(['remove', no_ask, package])

    def __get_repo_ids(self, repoinfo_extra_args: List[str] = None) -> List[str]:
        repoinfo_args: List[str] = ['--quiet', '-y']

        if repoinfo_extra_args:
            repoinfo_args.extend(repoinfo_extra_args)

        output = self.run(['repoinfo'] + repoinfo_args).stdout
        repo_ids: List[str] = []

        for line in output.splitlines():
            if 'Repo-id' in line:  # e.g. `Repo-id            : epel`
                repo_ids.append(line.split(':')[1].strip())

        return repo_ids

    def is_repo_enabled(self, repo: str) -> bool:
        enabled_repos = self.__get_repo_ids()

        if repo in enabled_repos:
            return True

        return False

    def are_repos_enabled(self, repos: List[str]) -> bool:
        enabled_repos: List[str] = self.__get_repo_ids()
        return all(repo in enabled_repos for repo in repos)

    def accept_keys(self):
        # to accept import of repo's GPG key (for repo_gpgcheck=1)
        self.run(['repolist', '-y'])

    def is_repo_available(self, repo: str) -> bool:
        retval = self.run(['repoinfo',
                           '--disablerepo=*',
                           f'--enablerepo={repo}',
                           '--quiet']).returncode

        if retval == 0:
            return True

        return False

    def makecache(self, timer: bool = True,
                  assume_yes: bool = True):
        args: List[str] = ['makecache']

        if timer:
            args.append('timer')

        if assume_yes:
            args.append('-y')

        self.run(args)

    def list_all_repos_info(self) -> List[Dict[str, str]]:
        """
        Query repoinfo and construct info per repository.
        """
        args: List[str] = ['repoinfo',
                           '--all',
                           '--quiet',
                           '-y']
        raw_output = self.run(args).stdout
        elems: List[str] = list(raw_output.split('\n\n'))
        repoinfo: List[List[str]] = [{} for _ in range(len(elems))]

        for elem_idx, elem in enumerate(elems):
            for line in elem.split('\n'):
                if line:
                    key, value = line.split(':', 1)
                    repoinfo[elem_idx][key.strip()] = value.strip()

        return repoinfo
