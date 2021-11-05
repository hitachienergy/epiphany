import logging


class CriticalError(Exception):
    """
    Raised when there was an error that could not be fixed by
    download-requirements script.
    """

    def __init__(self, msg: str):
        super().__init__()
        logging.error(msg)
