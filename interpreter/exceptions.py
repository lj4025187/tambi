class CommandNotInThisModule(Exception):
    pass
    #def __init__(self, value):
        #self.value = value
        
    #def __str__(self):
        #return repr(self.value)

class ClearCalled(Exception):
    pass

class SnapshotCalled(Exception):
    pass
