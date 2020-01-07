import sys

def input_query(question):

    while True:
        sys.stdout.write(question)
        input_text = input()
        if input_text != '':
            return input_text 
        else:
            sys.stdout.write(question)
            sys.stdout.write("\n")