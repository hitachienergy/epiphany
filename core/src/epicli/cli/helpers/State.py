class State:
    class __StateBase:
        OUTPUT_DIR = ''

        def __init__(self):
            self.OUTPUT_DIR = ''

    instance = None

    def __new__(cls, logger_name):
        if State.instance is None:
            State.instance = State.__StateBase()
        return State.instance
