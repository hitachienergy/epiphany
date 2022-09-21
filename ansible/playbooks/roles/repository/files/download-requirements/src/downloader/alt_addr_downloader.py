from pathlib import Path
from src.downloader.base_downloader import BaseDownloader


class AltAddrDownloader(BaseDownloader):
    """
    Requirements with provided alternative secondary address.
    """

    def download(self, requirement: str,
                       requirement_file: Path,
                       index: int,
                       sub_key: str = None,
                       additional_args: dict = None) -> bool:
        """
        Download `requirement` as `requirement_file` and compare checksums.

        :param requirement: an entry from the requirements corresponding to the downloaded file
        :param requirement_file: existing requirement file
        :param index: which entry in _requirements
        :param sub_key: optional keys for the `requirement` such as `url`
        :param additional_args: optional arguments passed to `download_func`
        :raises:
            :class:`ChecksumMismatch`: can be raised on failed checksum
        :returns: True - file downloaded correctly and/or checksum matched, False - otherwise
        """
        req = self._requirements[requirement]['options'][index]
        addr = req[sub_key] if sub_key else req
        return self._download(req, addr, requirement_file, additional_args)
