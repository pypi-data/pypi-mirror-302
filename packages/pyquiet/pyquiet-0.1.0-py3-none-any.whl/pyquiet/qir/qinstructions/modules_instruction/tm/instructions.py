from typing import Union, List
from pyquiet.qir.qinstructions.insn_base import InsnBase
from pyquiet.qir.qvariable import QuietVariable, PhyQubit
from pyquiet.qir.qmodule.modules import Module
from pyquiet.qir.qliteral import Time, Port


###########################################
#       Data Transfer Instructions        #
###########################################
class TimeDataTrans(InsnBase):
    def __init__(
        self, 
        opname, 
        dst_operand: QuietVariable, 
        src_operand
    ) -> None:
        super().__init__(opname)
        self.__dst_operand = dst_operand
        self.__src_operand = src_operand
        self.__module = Module.tm

    @property
    def module(self):
        return self.__module

    @property
    def dst(self) -> QuietVariable:
        return self.__dst_operand
    
    @property
    def src(self):
        return self.__src_operand

    def __str__(self):
        return f"{self.opname} {self.__dst_operand}, {self.__src_operand}"
            
class Ldt(TimeDataTrans):
    def __init__(
        self, 
        dst_operand: QuietVariable, 
        src_operand: Time
    ) -> None:
        super().__init__("ldt", dst_operand, src_operand)

class Movt(TimeDataTrans):
    def __init__(
        self, 
        dst_operand: QuietVariable, 
        src_operand: QuietVariable
    ) -> None:
        super().__init__("movt", dst_operand, src_operand)
            

###########################################
#         Arithmetic Instructions         #
###########################################
class TimeArithmeticOp(InsnBase):
    def __init__(
        self,
        operation: str,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2
    ) -> None:
        super().__init__(operation)
        self.__dst_operand = dst_operand
        self.__src_operand1 = src_operand1
        self.__src_operand2 = src_operand2
        self.__module = Module.tm

    @property
    def module(self):
        return self.__module

    @property
    def src1(self) -> QuietVariable:
        return self.__src_operand1

    @property
    def src2(self):
        return self.__src_operand2

    @property
    def dst(self) -> QuietVariable:
        return self.__dst_operand

    def __str__(self) -> str:
        return f"{self.opname} {self.__dst_operand}, {self.__src_operand1}, {self.__src_operand2}"


class Addt(TimeArithmeticOp):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("addt", dst_operand, src_operand1, src_operand2)

class Subt(TimeArithmeticOp):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("subt", dst_operand, src_operand1, src_operand2)

class Mult(TimeArithmeticOp):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("mult", dst_operand, src_operand1, src_operand2)

class Divt(TimeArithmeticOp):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("divt", dst_operand, src_operand1, src_operand2)

class Addti(TimeArithmeticOp):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: Time
    ) -> None:
        super().__init__("addti", dst_operand, src_operand1, src_operand2)

class Subti(TimeArithmeticOp):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: Time
    ) -> None:
        super().__init__("subti", dst_operand, src_operand1, src_operand2)

class Multi(TimeArithmeticOp):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: Union[int, float]
    ) -> None:
        super().__init__("multi", dst_operand, src_operand1, src_operand2)

class Divti(TimeArithmeticOp):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: Union[int, float]
    ) -> None:
        super().__init__("divti", dst_operand, src_operand1, src_operand2)

###########################################
#            Wait Instructions            #
###########################################
class WaitInsBase(InsnBase):
    def __init__(
        self, 
        opname: str,
        dst_operand,
        src_operand
    ) -> None:
        super().__init__(opname)
        self.__dst_operand = dst_operand
        self.__src_operand = src_operand
        self.__module = Module.tm

    @property
    def module(self):
        return self.__module

    @property
    def dst(self):
        return self.__dst_operand
    
    @property
    def src(self):
        return self.__src_operand
    
    def __str__(self) -> str:
        return f"{self.opname} {self.__dst_operand}, {self.__src_operand}"
    
class Waiti(WaitInsBase):
    def __init__(
        self,
        dst_operand: Port, 
        src_operand: Time
    ) -> None:
        super().__init__("waiti", dst_operand, src_operand)

class Wait(WaitInsBase):
    def __init__(
        self, 
        dst_operand: Port, 
        src_operand: QuietVariable
    ) -> None:
        super().__init__("wait", dst_operand, src_operand)

class Waitq(WaitInsBase):
    def __init__(
        self, 
        dst_operand: PhyQubit, 
        src_operand: QuietVariable
    ) -> None:
        super().__init__("waitq", dst_operand, src_operand)

class Waitqi(WaitInsBase):
    def __init__(
        self, 
        dst_operand: PhyQubit, 
        src_operand: Time
    ) -> None:
        super().__init__("waitqi", dst_operand, src_operand)

###########################################
#            Sync Instructions            #
###########################################
class SyncInsBase(InsnBase):
    def __init__(
        self, 
        opname: str,
        operands: list
    ) -> None:
        super().__init__(opname)
        self.__operands = operands
        self.__module = Module.tm

    @property
    def module(self):
        return self.__module

    @property
    def operands(self) -> list:
        return self.__operands
    
    def __str__(self) -> str:
        operands_str = ", ".join([str(operand) for operand in self.__operands])
        return f"{self.opname} {operands_str}"
    
class Sync(SyncInsBase):
    def __init__(
        self, 
        operands: List[Port]
    ) -> None:
        super().__init__("sync", operands)
        
class Syncq(SyncInsBase):
    def __init__(
        self, 
        operands: List[PhyQubit]
    ) -> None:
        super().__init__("syncq", operands)