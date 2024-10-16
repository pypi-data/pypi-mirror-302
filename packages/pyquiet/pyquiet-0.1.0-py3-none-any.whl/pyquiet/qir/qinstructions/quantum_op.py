import numpy as np
from typing import List
from pyquiet.qir.qgate.gate import DefGateConfig
from pyquiet.qir.qvariable import QuietVariable

class QuantumOp:
    def __init__(self, config: DefGateConfig, operands : List[QuietVariable] ) -> None:
        self.__config = config
        self.__operands = operands
        
    @property
    def operation(self) -> str:
        return self.__config.operation

    @property
    def matrix(self) -> np.ndarray:
        return self.__config.matrix
    
    @property
    def qubits(self) -> List[QuietVariable]:
        return self.__operands
    
    def __str__(self) -> str:
        return f"{self.operation} {', '.join([str(q) for q in self.qubits])}"