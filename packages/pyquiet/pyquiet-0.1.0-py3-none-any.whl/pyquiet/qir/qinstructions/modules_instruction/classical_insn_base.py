from __future__ import annotations
from pyquiet.qir.qinstructions.insn_base import InsnBase
from pyquiet.qir.qvariable import QuietVariable
from pyquiet.qir.qmodule.modules import Module


class ArithmeticOpBase(InsnBase):
    def __init__(
        self,
        operation: str,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable | int | float,
        module : Module
    ) -> None:
        super().__init__(operation)
        self.__dst_operand = dst_operand
        self.__src_operand1 = src_operand1
        self.__src_operand2 = src_operand2
        self.__module = module

    @property
    def module(self):
        return self.__module

    @property
    def src1(self) -> QuietVariable:
        return self.__src_operand1

    @property
    def src2(self) -> QuietVariable | int | float:
        return self.__src_operand2

    @property
    def dst(self) -> QuietVariable:
        return self.__dst_operand

    def __str__(self) -> str:
        return f"{self.opname} {self.__dst_operand}, {self.__src_operand1}, {self.__src_operand2}"


class BranchOpBase(InsnBase):
    def __init__(
        self,
        operation: str,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable,
        dst_label: str,
        module : Module
    ) -> None:
        super().__init__(operation)

        self.__src_operand1 = src_operand1
        self.__src_operand2 = src_operand2
        self.__dst_label = dst_label
        self.__module = module

    @property
    def module(self):
        return self.__module

    @property
    def src1(self) -> QuietVariable:
        return self.__src_operand1

    @property
    def src2(self) -> QuietVariable:
        return self.__src_operand2

    @property
    def dst_label(self) -> str:
        return self.__dst_label

    def __str__(self) -> str:
        return f"{self.opname} {self.__src_operand1}, {self.__src_operand2}, {self.__dst_label}"

class DataTransInsnBase(InsnBase):
    def __init__(
        self, 
        opname, 
        dst_operand: QuietVariable, 
        src_operand: QuietVariable | int | float,
        module : Module
    ) -> None:
        super().__init__(opname)
        self.__dst_operand = dst_operand
        self.__src_operand = src_operand
        self.__module = module

    @property
    def module(self):
        return self.__module

    @property
    def dst(self) -> QuietVariable:
        return self.__dst_operand
    
    @property
    def src(self) -> QuietVariable | int | float:
        return self.__src_operand

    def __str__(self):
        return f"{self.opname} {self.__dst_operand}, {self.__src_operand}"
            
class TypeConvInsnBase(InsnBase):
    def __init__(
        self, 
        opname, 
        dst_operand: QuietVariable, 
        src_operand: QuietVariable,
        module : Module
    ) -> None:
        super().__init__(opname)
        self.__dst_operand = dst_operand
        self.__src_operand = src_operand
        self.__module = module

    @property
    def module(self):
        return self.__module

    @property
    def dst(self) -> QuietVariable:
        return self.__dst_operand
    
    @property
    def src(self) -> QuietVariable:
        return self.__src_operand

    def __str__(self):
        return f"{self.opname} {self.__dst_operand}, {self.__src_operand}"
            
class LogicInsnBase(InsnBase):
    def __init__(
        self, 
        module : Module,
        opname, 
        dst_operand: QuietVariable, 
        src_operand1: QuietVariable,
        src_operand2: QuietVariable = None  
    ) -> None:
        super().__init__(opname)
        self.__dst_operand = dst_operand
        self.__src_operand1 = src_operand1
        self.__src_operand2 = src_operand2
        self.__module = module

    @property
    def module(self):
        return self.__module

    @property
    def dst(self) -> QuietVariable:
        return self.__dst_operand
    
    @property
    def src1(self) -> QuietVariable:
        return self.__src_operand1

    @property
    def src2(self) -> QuietVariable:
        return self.__src_operand2

    def __str__(self):
        if self.__src_operand2 is not None:
            return f"{self.opname} {self.__dst_operand}, {self.__src_operand1}, {self.__src_operand2}"
        else:
            return f"{self.opname} {self.__dst_operand}, {self.__src_operand1}"
        