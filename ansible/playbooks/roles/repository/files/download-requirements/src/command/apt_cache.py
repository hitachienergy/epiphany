from typing import List

from src.command.command import Command


class AptCache(Command):
    """
    Interface for `apt-cache` tool.
    """
    def __init__(self, retries: int):
        super().__init__('apt-cache', retries)

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
