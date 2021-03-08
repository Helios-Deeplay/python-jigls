class Base:
    """Concerete base class for all types of nodes and edges"""

    def __init__(
        self,
        # nid: str,
        name: str,
        dirty: bool,
        enable: bool,
    ):
        # self.nid = nid
        self.name = name
        self.dirty = dirty
        self.enable = enable

    def isDirty(self) -> bool:
        return self.dirty

    def isEnabled(self) -> bool:
        return self.enable

    def setDirty(self, flag: bool):
        self.dirty = flag

    def setEnable(self, flag=bool):
        self.enable = flag