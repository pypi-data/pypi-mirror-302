from typing import Union
from pyquiet.qir.qinstructions.modules_instruction.fm.instructions import (
    Ldd, Movd, Addd, Subd, Muld, Divd, Adddi, Subdi, Muldi, Divdi, Casti, Castd)

QuietFmInstruction = Union[
    Ldd, Movd, Addd, Subd, Muld, Divd, Adddi, Subdi, Muldi, Divdi, Casti, Castd
]