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
            version = version.rstrip('*')
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
        show_args: List[str] = ['show', f'{package}={version}' if version else package]
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

    @staticmethod
    def __parse_apt_cache_depends(stdout: str) -> List[str]:
        """
        Parse output from `apt-cache depends`.
        For deps with alternative, only the first package is choosen.
        Virtual packages are replaced by the first candidate.

        :param stdout: output from `apt-cache depends` command
        :returns: required dependencies
        """
        alternative_found = False
        is_alternative = False
        virt_pkg_found = False
        deps: List[str] = []
        for dep in stdout.strip().splitlines():

            dep = dep.replace(' ', '')  # remove white spaces

            if virt_pkg_found and not is_alternative:
                deps.append(dep)  # pick first from the list
                virt_pkg_found = False

            if 'Depends:' in dep:  # dependency found
                is_alternative = alternative_found
                alternative_found = dep.startswith('|Depends:')
                virt_pkg_found = '<' in dep and '>' in dep

                if not virt_pkg_found and not is_alternative:
                    dep = dep.split('Depends:')[-1]  # remove "Depends:
                    deps.append(dep)

        return deps

    def get_package_dependencies(self, package: str, version: str = '') -> List[str]:
        """
        Interface for `apt-cache depends`

        :param package: for which dependencies will be gathered
        :param version: optional argument to use specific `package`'s version
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
                           f'{package}={version}' if version else package]

        raw_output = self.run(args).stdout
        return self.__parse_apt_cache_depends(raw_output)
