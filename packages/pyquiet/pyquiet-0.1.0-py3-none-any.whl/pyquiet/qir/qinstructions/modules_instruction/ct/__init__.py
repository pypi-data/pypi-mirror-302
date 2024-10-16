from typing import Union
from pyquiet.qir.qinstructions.modules_instruction.ct.instructions import (
    Jump, Bne, Beq, Bgt, Bge, Blt, Ble)

QuietCTInstructions = Union[
    Jump, Bne, Beq, Bgt, Bge, Blt, Ble]