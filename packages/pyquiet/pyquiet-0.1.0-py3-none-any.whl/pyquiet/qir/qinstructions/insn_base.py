
class InsnBase:
    def __init__(
            self, 
            opname : str,
    ) -> None:
        self.__opname = opname
    
    @property
    def opname(self):
        return self.__opname