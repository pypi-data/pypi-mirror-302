from typing import List, Union
from pyquiet.qir.qvariable import NonListVariable, ListVariable

###########################################
#        About Control Key Words.         #
###########################################


class ControlWords:
    def __init__(self) -> None:
        self.__ctrl = False
        # the control qubit is only one qubit.
        self.__qubits: List[Union[NonListVariable, ListVariable.ListElement]] = None

    def set_ctrl(self) -> None:
        self.__ctrl = True

    @property
    def ctrl(self) -> bool:
        return self.__ctrl

    def set_qubits(self, qubits: List[Union[NonListVariable, ListVariable.ListElement]]) -> None:
        self.__qubits = qubits

    @property
    def ctrl_qubits(self) -> List[Union[NonListVariable, ListVariable.ListElement]]:
        return self.__qubits
