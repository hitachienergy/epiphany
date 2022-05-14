import logging


class DownloadRequirementsError(Exception):
    """
    Base class for all non standard errors raised during a script run.
    """
    def __init__(self, msg: str):
        super().__init__()
        logging.error(msg)


class CriticalError(DownloadRequirementsError):
    """
    Raised when there was an error that could not be fixed by
    download-requirements script.
    """


class DnfVariableNotfound(CriticalError):
    """
    Raised when DNF variable was not found.
    """


class PackageNotfound(CriticalError):
    """
    Raised when there was no package found by the query tool.
    """


class ChecksumMismatch(DownloadRequirementsError):
    """
    Raised when there was a file checksum mismatch.
    """
    def __init__(self, msg: str):
        super().__init__(f'{msg} - download failed due to checksum mismatch, '
                         'WARNING someone might have replaced the file')
