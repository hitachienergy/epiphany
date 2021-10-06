"""Path related Epiphany filters"""

import os.path


def get_parent_paths(path, exclude=None):
    """
    Returns all parent paths in bottom-up order
    example: '/var/log/file' -> ['/var/log', '/var', '/']
    :param path: path to file or dir (existence doesn't matter)
    :type path: str
    :param exclude: paths to exclude, defaults to ['/']
    :type exclude: list, optional
    :return: parent paths
    :rtype: list
    """
    excluded_paths = exclude or ['/']
    paths = []
    while path != '/':
        path = os.path.dirname(path)
        if path not in excluded_paths:
            paths.append(path)
    return paths


# ---- Ansible filters ----
class FilterModule(object):
    """Defines filters"""

    def filters(self):
        # pylint: disable=no-self-use
        return {
            'parent_paths': get_parent_paths
        }
