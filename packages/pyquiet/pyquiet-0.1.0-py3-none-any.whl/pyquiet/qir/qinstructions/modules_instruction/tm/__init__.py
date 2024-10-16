from typing import Union
from pyquiet.qir.qinstructions.modules_instruction.tm.instructions import (
    Ldt, Movt, Addti, Addt, Subti, Subt, Multi, Mult, Divti, Divt, Waiti, Wait, Waitq, Waitqi, Sync, Syncq)

QuietTmInstruction = Union[
    Ldt, Movt, Addti, Addt, Subti, Subt, Multi, Mult, Divti, Divt, Waiti, Wait, Waitq, Waitqi, Sync, Syncq]