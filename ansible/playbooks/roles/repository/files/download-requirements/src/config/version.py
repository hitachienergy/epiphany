class Version:
    """
    Type used in comparing epiphany version.
    """

    def __init__(self, ver: str):
        major, minor, patch = ver.split('.')
        self.major: int = int(major)
        self.minor: int = int(minor)
        self.patch: int = int(''.join(filter(lambda char: char.isdigit(), patch)))  # handle `1dev`, `2rc`, etc.

    def __lt__(self, rhs):
        if self.major < rhs.major:
            return True

        if self.major == rhs.major:
            if self.minor < rhs.minor:
                return True

            if self.minor == rhs.minor:
                if self.patch < rhs.patch:
                    return True

        return False
