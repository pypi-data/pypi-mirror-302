from typing import Union
from pyquiet.qir.qinstructions.modules_instruction.im.instructions import (
    Ld, Mov, Lnot, Land, Lor, Lxor, Add, Sub, Mul, Div, Addi, Subi, Muli, Divi)


QuietImInstruction = Union[
    Ld, Mov, Lnot, Land, Lor, Lxor, Add, Sub, Mul, Div, Addi, Subi, Muli, Divi]