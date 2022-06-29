import argparse


# Used by multiple epicli parsers
def comma_separated_type(choices):
    """Return a function that splits and checks comma-separated values."""
    def split_arg(arg):
        values = arg.replace(' ', '').lower().split(',')
        for value in values:
            if value not in choices:
                raise argparse.ArgumentTypeError(
                    f'invalid choice: {value!r} (choose from {", ".join([repr(choice) for choice in choices])})')
        return values
    return split_arg
