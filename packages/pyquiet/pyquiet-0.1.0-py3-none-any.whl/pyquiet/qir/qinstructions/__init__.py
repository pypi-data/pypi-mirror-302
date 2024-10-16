from typing import Union
from pyquiet.qir.qinstructions.func_call import FuncCall
from pyquiet.qir.qinstructions.var_decl import VarDecl
from pyquiet.qir.qinstructions.label import Label
from pyquiet.qir.qinstructions.quantum_op import QuantumOp

from pyquiet.qir.qinstructions.modules_instruction.ct import QuietCTInstructions
from pyquiet.qir.qinstructions.modules_instruction.fm import QuietFmInstruction
from pyquiet.qir.qinstructions.modules_instruction.im import QuietImInstruction
from pyquiet.qir.qinstructions.modules_instruction.std import QuietStdInstruction, ControlWords
from pyquiet.qir.qinstructions.modules_instruction.pm import QuietPmInstruction
from pyquiet.qir.qinstructions.modules_instruction.tm import QuietTmInstruction

QiInstruction = Union[VarDecl, FuncCall, QuietStdInstruction, QuietCTInstructions, QuietImInstruction, QuietFmInstruction, QuietPmInstruction, QuietTmInstruction]


