class Base:
    """Concerete base class for all types of nodes, edges, graph"""

    def __init__(
        self,
        # nid: str,
        name: str,
        dirty: bool = False,
        enable: bool = True,
    ):
        self.name = name
        self.dirty = dirty
        self.enable = enable

    def IsDirty(self) -> bool:
        return self.dirty

    def IsEnabled(self) -> bool:
        return self.enable

    def SetName(self, value: str):
        self.name = value