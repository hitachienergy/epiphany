from hashlib import sha1, sha256
from pathlib import Path
from typing import Callable, Dict


def get_hash(req_path: Path, algorithm: Callable) -> str:
    """
    Calculate hash value for `req_path` file using `algorithm`.

    :param req_path: of which file to calculate hash
    :param algorithm: hash algorithm to be used
    :returns: calculated hash value, "-1" if file not found
    """
    try:
        with open(req_path, mode='rb') as req_file:
            hashgen = algorithm()
            hashgen.update(req_file.read())
            return hashgen.hexdigest()
    except FileNotFoundError:
        return "-1"


def get_sha256(req_path: Path) -> str:
    return get_hash(req_path, sha256)


def get_sha1(req_path: Path) -> str:
    """ For larger files sha1 algorithm is significantly faster than sha256 """
    return get_hash(req_path, sha1)


SHA_ALGORITHMS: Dict[str, Callable] = {
    'sha1': get_sha1,
    'sha256': get_sha256
}
