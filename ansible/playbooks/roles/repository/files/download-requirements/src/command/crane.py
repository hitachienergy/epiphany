from pathlib import Path
from typing import List

from src.command.command import Command


class Crane(Command):
    """
    Interface for Crane
    """

    def __init__(self, retries: int):
        super().__init__('crane', retries)

    def pull(self, image_name: str,
             destination: Path,
             platform: str,
             use_legacy_format: bool = False,
             insecure: bool = False):
        """
        Download target image file

        :param image_name: address to the image
        :param destination: where to store the downloaded image
        :param platform: for which platform file will be downloaded
        :param use_legacy_format: use legacy format
        :param insecure: allow image references to be fetched without TLS
        """
        crane_params: List[str] = ['pull']

        if insecure:
            crane_params.append('--insecure')

        crane_params.append(f'--platform={platform}')

        crane_format = 'legacy' if use_legacy_format else 'tarball'
        crane_params.append(f'--format={crane_format}')

        crane_params.append(image_name)
        crane_params.append(str(destination))
        self.run(crane_params)
