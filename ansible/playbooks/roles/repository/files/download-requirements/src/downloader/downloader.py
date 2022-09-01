from pathlib import Path

from src.downloader.base_downloader import BaseDownloader
from src.error import ChecksumMismatch


class Downloader(BaseDownloader):
    def download(self, requirement: str, requirement_file: Path, sub_key: str = None, additional_args: dict = None):
        """
        Download `requirement` as `requirement_file` and compare checksums.

        :param requirement: an entry from the requirements corresponding to the downloaded file
        :param requirement_file: existing requirement file
        :param sub_key: optional keys for the `requirement` such as `url`
        :param additional_args: optional arguments passed to `download_func`
        :raises:
            :class:`ChecksumMismatch`: can be raised on failed checksum
        """
        req = self._requirements[requirement]
        addr = req[sub_key] if sub_key else requirement
        self._download(req, addr, requirement_file, additional_args)
