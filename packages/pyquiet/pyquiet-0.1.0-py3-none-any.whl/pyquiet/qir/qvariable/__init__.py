from typing import Union
from pyquiet.qir.qvariable.variable import ListVariable, NonListVariable, QuietType, PhyQubit

QuietVariable = Union[NonListVariable, ListVariable, ListVariable.ListElement, PhyQubit]
