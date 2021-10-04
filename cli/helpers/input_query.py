import getpass

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