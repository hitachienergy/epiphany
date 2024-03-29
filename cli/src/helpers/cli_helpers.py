import getpass
import sys

from cli.src.Config import Config


def prompt_for_value(prompt):
    input_text = ''
    while input_text == '':
        input_text = input(prompt)
    return input_text


def prompt_for_password(prompt):
    password = ''
    while password == '':
        password = getpass.getpass(prompt)
    return password


def query_yes_no(question, default="yes"):
    if Config().auto_approve:
        return True

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
