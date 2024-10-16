from pyquiet.qir.qvariable import QuietVariable
from pyquiet.qir.qinstructions.modules_instruction.classical_insn_base import ArithmeticOpBase, DataTransInsnBase, LogicInsnBase
from pyquiet.qir.qmodule.modules import Module


###########################################
#       Data Transfer Instructions        #
###########################################
class Ld(DataTransInsnBase):
    def __init__(
        self, 
        dst_operand: QuietVariable, 
        src_operand: int
    ) -> None:
        super().__init__("ld", dst_operand, src_operand, Module.im)

    @property
    def imm(self):
        return self.src

class Mov(DataTransInsnBase):
    def __init__(
        self, 
        dst_operand: QuietVariable, 
        src_operand: QuietVariable
    ):
        super().__init__("mov", dst_operand, src_operand, Module.im)


###########################################
#            Logic Instructions           #
###########################################
class Lnot(LogicInsnBase):
    def __init__(
        self, 
        dst_operand: QuietVariable, 
        src_operand: QuietVariable
    ) -> None:
        super().__init__(Module.im, "lnot", dst_operand, src_operand)

    @property
    def src(self) -> QuietVariable:
        return self.src1

class Land(LogicInsnBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__(Module.im, "land", dst_operand, src_operand1, src_operand2)

class Lor(LogicInsnBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__(Module.im, "lor", dst_operand, src_operand1, src_operand2)

class Lxor(LogicInsnBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__(Module.im, "lxor", dst_operand, src_operand1, src_operand2)


###########################################
#         Arithmetic Instructions         #
###########################################


class Add(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("add", dst_operand, src_operand1, src_operand2, Module.im)

class Sub(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("sub", dst_operand, src_operand1, src_operand2, Module.im)

class Mul(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("mul", dst_operand, src_operand1, src_operand2, Module.im)

class Div(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("div", dst_operand, src_operand1, src_operand2, Module.im)

class Addi(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: int
    ) -> None:
        super().__init__("addi", dst_operand, src_operand1, src_operand2, Module.im)

class Subi(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: int
    ) -> None:
        super().__init__("subi", dst_operand, src_operand1, src_operand2, Module.im)

class Muli(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: int
    ) -> None:
        super().__init__("muli", dst_operand, src_operand1, src_operand2, Module.im)

class Divi(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: int
    ) -> None:
        super().__init__("divi", dst_operand, src_operand1, src_operand2, Module.im)
