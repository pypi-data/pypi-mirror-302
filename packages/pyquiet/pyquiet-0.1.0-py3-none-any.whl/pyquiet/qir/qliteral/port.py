from typing import List
from enum import Enum


class PortType(Enum):
    logical = 0
    physical = 1


class Port:
    def __init__(self, type: PortType, port_literal: List[str]) -> None:
        self.__type = type
        self.__port_literal: List[str] = port_literal

    @property
    def port_literal(self):
        return self.__port_literal

    def __str__(self) -> str:
        port_sym = ["$", "#"]
        return port_sym[self.__type.value] + ":".join(self.__port_literal)
