from itertools import chain
from typing import Any, Dict, List


class FilterModule:
    """ Filters for Python's container types """

    def filters(self):
        return {
            'dict_to_list': self.dict_to_list,
            'flatten_list': self.flatten_list,
        }

    def dict_to_list(self, data: Dict, only_values: bool = False, only_keys: bool = False) -> List:
        """
        Convert dict to list without using Ansible's loop mechanism with dict2items filter.

        :param data: to be converted into a list
        :param only_values: construct list with only dict's values
        :param only_keys: construct list with only dict's keys
        :return: data transformed into a list
        """
        if only_values:
            return list(data.values())

        if only_keys:
            return list(data.keys())

        return list(data.items())

    def flatten_list(self, data: List[List[Any]]) -> Any:
        """
        Flatten list of lists to a single list with elements

        :param data: to be flatten
        :return: list of elements
        """
        return list(chain(*data))
