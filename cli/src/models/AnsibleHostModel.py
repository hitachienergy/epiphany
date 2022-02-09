class AnsibleHostModel:
    def __init__(self, name: str, ip: str):
        self.name: str = name
        self.ip: str = ip

    def __eq__(self, other) -> bool:
        return (self.name == other.name and
                self.ip == other.ip)

    def __lt__(self, other) -> bool:
        pass


class AnsibleOrderedHostModel(AnsibleHostModel):
    """
    Sortable variant of AnsibleHostModel
    """

    def __lt__(self, other) -> bool:
        return self.name < other.name
