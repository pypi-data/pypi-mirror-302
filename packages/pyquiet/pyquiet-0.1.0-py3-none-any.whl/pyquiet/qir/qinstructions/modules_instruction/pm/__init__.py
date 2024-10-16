from typing import Union
from pyquiet.qir.qinstructions.modules_instruction.pm.cus_pm_insn import CusWaveInsn, DefWaveInsn
from pyquiet.qir.qinstructions.modules_instruction.pm.instructions import (
    Square, Cos, Sin, Gaussian, Drag, Ramp,
    Addp, Subp, Mulp, Convp, Joinp, Scalep, Flipp, Cutp,
    Setfreq, Shiftphase, Setphase, Play, Playmod, CapSignal, CapBit)

QuietPmInstruction = Union[
    Square, Cos, Sin, Gaussian, Drag, Ramp,
    Addp, Subp, Mulp, Convp, Joinp, Scalep, Flipp, Cutp,
    Setfreq, Shiftphase, Setphase, Play, Playmod, CapSignal, CapBit]