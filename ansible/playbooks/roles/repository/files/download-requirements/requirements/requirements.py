from typing import Dict, List
from src.config import OSArch, OSType
from requirements.ubuntu import REQUIREMENTS_X86_64 as Ubuntu_X86_64


REQUIREMENTS: Dict[OSArch, Dict[OSType, Dict[str, List]]] = {
    OSArch.X86_64: {
        OSType.CentOS: {},
        OSType.RedHat: {},
        OSType.Ubuntu: Ubuntu_X86_64
    },
    OSArch.ARM64: {
        OSType.CentOS: {}
    }
}
