from typing import Dict,List
from pyquiet.qir.qgate.gate import DefGateConfig

class GateSection:
    def __init__(self) -> None:
        self.__gate_table: Dict[str, DefGateConfig] = {}

    @property
    def dict(self):
        return self.__gate_table

    def is_defined_gate(self, gate_name:str):
        if gate_name in self.__gate_table:
            return True
        else:
            return False

    def define_gate(self, gate_config: DefGateConfig):
        if self.__gate_table.get(gate_config.operation) != None:
            raise ValueError(f"The quantum gate {gate_config.operation} has been already defined.")
        self.__gate_table[gate_config.operation] = gate_config

    def get_config(self, gate_name: str) -> DefGateConfig:
        config = self.__gate_table.get(gate_name)
        if config == None:
            raise ValueError(f"The quantum gate {gate_name} is not defined yet.")
        return config
    
    def __str__(self) -> str:
        return ".gate:\n\t" + "\n\t".join(str(gatestr) for gatestr in self.__gate_table.values())
    
    def __len__(self) -> str:
        return len(self.__gate_table)