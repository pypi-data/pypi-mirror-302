from pyquiet.qir.qvariable import QuietVariable
from pyquiet.qir.qinstructions.insn_base import InsnBase
from pyquiet.qir.qinstructions.modules_instruction.classical_insn_base import BranchOpBase
from pyquiet.qir.qmodule.modules import Module

###########################################
#       Branch and Jump Instruction       #
###########################################
class Jump(InsnBase):
    def __init__(self, dst_label: str) -> None:
        super().__init__("jump")
        self.__dst_label = dst_label
        self.__module = Module.ct

    @property
    def module(self):
        return self.__module

    @property
    def dst_label(self) -> str:
        return self.__dst_label

    def __str__(self):
        return f"{self.opname} {self.__dst_label}"


class Bne(BranchOpBase):
    def __init__(
        self,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable,
        dst_label: str
    ) -> None:
        super().__init__("bne", src_operand1, src_operand2, dst_label, Module.ct)

class Beq(BranchOpBase):
    def __init__(
        self,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable,
        dst_label: str
    ) -> None:
        super().__init__("beq", src_operand1, src_operand2, dst_label, Module.ct)

class Bgt(BranchOpBase):
    def __init__(
        self,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable,
        dst_label: str
    ) -> None:
        super().__init__("bgt", src_operand1, src_operand2, dst_label, Module.ct)

class Bge(BranchOpBase):
    def __init__(
        self,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable,
        dst_label: str
    ) -> None:
        super().__init__("bge", src_operand1, src_operand2, dst_label, Module.ct)

class Blt(BranchOpBase):
    def __init__(
        self,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable,
        dst_label: str
    ) -> None:
        super().__init__("blt", src_operand1, src_operand2, dst_label, Module.ct)

class Ble(BranchOpBase):
    def __init__(
        self,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable,
        dst_label: str
    ) -> None:
        super().__init__("ble", src_operand1, src_operand2, dst_label, Module.ct)
