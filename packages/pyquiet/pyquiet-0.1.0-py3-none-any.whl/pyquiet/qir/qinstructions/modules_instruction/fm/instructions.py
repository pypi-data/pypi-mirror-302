from pyquiet.qir.qinstructions.modules_instruction.classical_insn_base import DataTransInsnBase, TypeConvInsnBase, ArithmeticOpBase, Module
from pyquiet.qir.qvariable import QuietVariable


###########################################
#       Data Transfer Instructions        #
###########################################
class Ldd(DataTransInsnBase):
    def __init__(
            self, 
            dst_operand: QuietVariable, 
            src_operand: float
    ) -> None:
        super().__init__("ldd", dst_operand, src_operand, Module.fm)

    @property
    def imm(self) -> float:
        return self.src


class Movd(DataTransInsnBase):
    def __init__(
            self, 
            dst_operand: QuietVariable, 
            src_operand: QuietVariable
    ):
        super().__init__("movd", dst_operand, src_operand, Module.fm)


###########################################
#         Arithmetic Instructions         #
###########################################
class Addd(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("addd", dst_operand, src_operand1, src_operand2, Module.fm)


class Subd(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("subd", dst_operand, src_operand1, src_operand2, Module.fm)

class Muld(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("muld", dst_operand, src_operand1, src_operand2, Module.fm)

class Divd(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: QuietVariable
    ) -> None:
        super().__init__("divd", dst_operand, src_operand1, src_operand2, Module.fm)

class Adddi(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: float
    ) -> None:
        super().__init__("adddi", dst_operand, src_operand1, src_operand2, Module.fm)

class Subdi(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: float
    ) -> None:
        super().__init__("subdi", dst_operand, src_operand1, src_operand2, Module.fm)

class Muldi(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: float
    ) -> None:
        super().__init__("muldi", dst_operand, src_operand1, src_operand2, Module.fm)

class Divdi(ArithmeticOpBase):
    def __init__(
        self,
        dst_operand: QuietVariable,
        src_operand1: QuietVariable,
        src_operand2: float
    ) -> None:
        super().__init__("divdi", dst_operand, src_operand1, src_operand2, Module.fm)


###########################################
#      Type Conversion Instructions       #
###########################################
class Casti(TypeConvInsnBase):
    def __init__(
            self, 
            dst_operand: QuietVariable, 
            src_operand: QuietVariable
    ):
        super().__init__("casti", dst_operand, src_operand, Module.fm)

class Castd(TypeConvInsnBase):
    def __init__(
            self, 
            dst_operand: QuietVariable, 
            src_operand: QuietVariable
    ):
        super().__init__("castd", dst_operand, src_operand, Module.fm)
