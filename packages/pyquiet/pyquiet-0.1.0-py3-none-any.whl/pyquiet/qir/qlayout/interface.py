from typing import List
from pyquiet.qir.qliteral.port import PortType, Port


class PortNode:
    def __init__(self, name: str, type: PortType, alias: str = None) -> None:
        if type == PortType.logical and alias is not None:
            raise ValueError("Logical port cannot have alias.")
        self.__name = name
        self.__alias = alias
        self.__type = type
        self.__subports = []

    @property
    def name(self):
        return self.__name

    @property
    def alias(self):
        return self.__alias

    @property
    def subports(self):
        return self.__subports

    @property
    def type(self):
        return self.__type

    def add_subports(self, subport_list: list):
        self.__subports.extend(subport_list)

    def __str__(self) -> str:
        port_str = (
            ("#" if self.__type == PortType.physical else "")
            + self.__name
            + (f"({self.__alias})" if self.__alias is not None else "")
        )
        return port_str


class QubitNode:
    def __init__(self, names: List[str]) -> None:
        self.__qubits = names
        self.__subports: List[PortNode] = []

    @property
    def qubits(self):
        return self.__qubits

    @property
    def subports(self):
        return self.__subports

    def add_subports(self, subport_list: List[PortNode]):
        self.__subports.extend(subport_list)

    def __str__(self) -> str:
        return "[" + "$" + ", $".join(self.__qubits) + "]"


class PortDeclaration:
    def __init__(self, qubits_node: QubitNode = None) -> None:
        self.__qubits_node = qubits_node

    @property
    def qubits_node(self):
        return self.__qubits_node

    def init_qubit_node(self, qubit_list: QubitNode):
        if self.__qubits_node is not None:
            raise ValueError("Qubit node already exists.")
        self.__qubits_node = qubit_list

    def walk_port_tree(self, node=None) -> str:
        if node is None:
            if self.__qubits_node is None:
                return ""
            node = self.__qubits_node

        string = str(node)
        child_string = ", ".join(
            [self.walk_port_tree(child) for child in node.subports]
        )
        if child_string != "":
            string += ":{" + child_string + "}"

        return string

    def __str__(self) -> str:
        return "port " + self.walk_port_tree()


class BindPort:
    def __init__(self, physical_port: Port, logic_port_list: List[Port]) -> None:
        self.__phyport = physical_port
        self.__lgcport_list = logic_port_list

    @property
    def phyport(self):
        return self.__phyport

    @property
    def lgcport_list(self):
        return self.__lgcport_list

    def __str__(self) -> str:
        lgcport_str = ", ".join([str(port) for port in self.__lgcport_list])
        return f"bind {self.__phyport}, [{lgcport_str}]"
