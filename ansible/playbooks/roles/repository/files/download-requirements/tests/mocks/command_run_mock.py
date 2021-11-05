import subprocess
from typing import Any, Callable, Dict, List
from unittest.mock import Mock

from pytest_mock.plugin import MockerFixture


class CommandRunMock:
    """
    Mock class for Command.run() calls.
    Usage:

    with CommandRunMock(mocker, function_to_test, function_args) as call_args:
        assert call_args == [expected_arg1, ...]
    """
    def __init__(self, mocker: MockerFixture, func: Callable, args: Dict[str, Any] = None):
        """
        :param mocker: mocker object provided by pytest
        :param func: function which will be tested
        :param args: parameters that will be passed to `__func`
        """
        self.__mocker = mocker
        self.__func = func
        self.__args = args

    def __enter__(self) -> List[str]:
        """
        :return: list of arguments passed to the subprocess.run() function
        """
        mock = Mock()
        mock.returncode = 0

        self.__mocker.patch('src.command.command.subprocess.run', side_effect=lambda args, encoding, stdout, stderr: mock)

        spy = self.__mocker.spy(subprocess, 'run')

        if self.__args:
            self.__func(**self.__args)
        else:
            self.__func()

        return spy.call_args[0][0]

    def __exit__(self, *args):
        pass
