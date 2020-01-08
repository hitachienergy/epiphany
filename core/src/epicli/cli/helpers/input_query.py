import sys

def prompt_for_value(prompt):
    input_text = ''
    while input_text == '':
        input_text = input(prompt)
    return input_text