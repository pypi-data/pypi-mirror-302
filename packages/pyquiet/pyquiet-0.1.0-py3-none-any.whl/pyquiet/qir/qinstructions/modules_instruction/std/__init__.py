from typing import Union
from pyquiet.qir.qinstructions.modules_instruction.std.control_words import ControlWords
from pyquiet.qir.qinstructions.modules_instruction.std.instructions import (
    H, X, Y, Z, S, T, Sdag, Tdag, CNOT, CZ, SWAP, Rx, Ry, Rz, Rxy, U4, CP, CRz)

QuietStdInstruction = Union[
    H, X, Y, Z, S, T, Sdag, Tdag, CNOT, CZ, SWAP, Rx, Ry, Rz, Rxy, U4, CP, CRz
]
