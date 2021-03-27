class Data(object):
    def __init__(self, value, flag=True):
        self.value = value
        self.enable = flag

    def GetData(self):
        return self.value

    def SetData(self, data):
        self.value = data

    def GetEnable(self):
        return self.enable

    def SetEnable(self, flag):
        self.enable = flag


class OptionalArg(str):
    def __repr__(self):
        return 'OptionalArg("%s")' % self

    pass


class DataPlaceholderNode(str):
    def __repr__(self):
        return 'DataPlaceholderNode("%s")' % self


class DeleteInstruction(str):
    def __repr__(self):
        return 'DeleteInstruction("%s")' % self