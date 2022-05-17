from typing import Dict, List

from src.command.command import Command
from src.error import CriticalError


class AptCache(Command):
    """
    Interface for `apt-cache` tool.
    """
    def __init__(self, retries: int):
        super().__init__('apt-cache', retries)

    def __get_package_candidate_version(self, package: str, version: str = '') -> str:
        """
        Use cache to find out `package` candidate version number.

        :param package: for which candidate version to return
        :param version: optional argument to use specific `package`'s version
        :raises:
            :class:`CriticalError`: can be raised when package candidate was not found
        :returns: candidate version number
        """
        policy_args: List[str] = ['policy', package]
        policy_output = self.run(policy_args).stdout

        output_lines: List[str] = policy_output.split('\n')
        if version:  # confirm that the wanted version is available
            for line in output_lines:
                if version in line:
                    return version
        else:
            for line in output_lines:  # get candidate version
                if 'Candidate' in line:
                    return line.split(': ')[-1]

        raise CriticalError(f'Candidate for {package} not found, command: `{self.command()}`')

    def get_package_info(self, package: str, version: str = '') -> Dict[str, str]:
        """
        Get cached data for `package` and return it in a formatted form.

        :param package: for which data to return
        :param version: optional argument to use specific `package`'s version
        :returns: structured cached `package` info
        """
        show_args: List[str] = ['show', package]
        show_output = self.run(show_args).stdout

        version_info: str = ''
        candidate_version: str = self.__get_package_candidate_version(package, version)
        for ver_info in show_output.split('\n\n'):
            if  candidate_version in ver_info:
                version_info = ver_info
                break

        info: Dict[str, str] = {}
        for line in version_info.split('\n'):
            if line:
                try:
                    key, value = line.split(': ')
                    info[key] = value
                except ValueError:
                    pass

        return info

    def get_package_dependencies(self, package: str) -> List[str]:
        """
        Interface for `apt-cache depends`

        :param package: for which dependencies will be gathered
        :returns: all required dependencies for `package`
        """
        args: List[str] = ['depends',
                           '--no-recommends',
                           '--no-suggests',
                           '--no-conflicts',
                           '--no-breaks',
                           '--no-replaces',
                           '--no-enhances',
                           '--no-pre-depends',
                           package]

        raw_output = self.run(args).stdout

        virt_pkg: bool = False  # True - virtual package detected, False - otherwise
        virt_pkgs: List[str] = []  # cached virtual packages options
        deps: List[str] = []
        for dep in raw_output.split('\n'):
            if not dep:  # skip empty lines
                continue

            dep = dep.replace(' ', '')  # remove white spaces

            if virt_pkg:
                virt_pkgs.append(dep)  # cache virtual package option

            if '<' in dep and '>' in dep:  # virtual package, more than one dependency to choose
                virt_pkg = True
                continue

            if 'Depends:' in dep:  # new dependency found
                virt_pkg = False

                if virt_pkgs:  # previous choices cached
                    # avoid conflicts by choosing only non-cached dependency:
                    if not any(map(lambda elem: elem in deps, virt_pkgs)):
                        deps.append(virt_pkgs[0].split('Depends:')[-1])  # pick first from the list
                    virt_pkgs.clear()

                dep = dep.split('Depends:')[-1]  # remove "Depends:

            if not virt_pkg and dep != package:  # avoid adding package itself
                    deps.append(dep)

        return list(set(deps))
