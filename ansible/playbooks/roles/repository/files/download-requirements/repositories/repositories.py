from typing import Dict, List

from repositories.ubuntu import REPOSITORIES_X86_64 as Ubuntu_X86_64
from src.config import OSArch, OSType


REPOSITORIES: Dict[OSArch, Dict[OSType, Dict[str, List]]] = {
    OSArch.X86_64: {
        OSType.CentOS: {},
        OSType.RedHat: {},
        OSType.Ubuntu: Ubuntu_X86_64
    },
    OSArch.ARM64: {
        OSType.CentOS: {}
    }
}
