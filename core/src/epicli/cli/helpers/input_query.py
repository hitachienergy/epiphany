import sys

def input_query(question):

    while True:
        sys.stdout.write(question)
        inputText = input()
        if inputText != '':
            return inputText
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")