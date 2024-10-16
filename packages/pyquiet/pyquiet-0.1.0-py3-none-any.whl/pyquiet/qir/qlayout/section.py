from typing import List
from pyquiet.qir.qlayout.interface import PortDeclaration, BindPort


class LayoutSection:
    def __init__(self) -> None:
        self.__portdecls_list: List[PortDeclaration] = []
        self.__bind_port_list: List[BindPort] = []

    @property
    def port_decl_list(self):
        return self.__portdecls_list

    @property
    def bind_port_list(self):
        return self.__bind_port_list

    def add_port_declaration(self, port_decl: PortDeclaration):
        self.__portdecls_list.append(port_decl)

    def add_bind_port_insn(self, bind_port: BindPort):
        self.__bind_port_list.append(bind_port)

    def __str__(self) -> str:
        portact_str = "\n\t".join(str(portact) for portact in self.__portdecls_list)
        bindact_str = "\n\t".join(str(bindact) for bindact in self.__bind_port_list)
        return f".layout:\n\t{portact_str}\n\t{bindact_str}"
