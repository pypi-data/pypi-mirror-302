from typing import List, Union
from pyquiet.qir.qmodule import ModuleSet, Module
from pyquiet.qir.qfile import FileSection, File
from pyquiet.qir.qgate import GateSection, DefGateConfig
from pyquiet.qir.qpulse import PulseSection, CustomWaveCfg, DefWaveCfg
from pyquiet.qir.qcode import CodeSection, Function
from pyquiet.qir.qentry import EntrySection
from pyquiet.qir.qinstructions import FuncCall
from pyquiet.qir.qlayout import LayoutSection, PortDeclaration, BindPort


class QiProgram:
    """
       QiProgram is the intermediate representation of a `qi` file.
    It can be transformed from a quiet AST(CST), and extract the more essential information.

    A Quiet program is composed of four sections:
    * Modules Section: Load different instruction modules to limit the module instruction set.
    * File Section: Include other `qi` files.
    * Gate Section: Define the quantum gates in matrix form.
    * Code Section: Describe the program codes with functions.
    * Entry Section: The entry point of the program.
    """

    def __init__(self, file_name: str) -> None:
        self.__file_name: str = file_name
        self.__module_set: ModuleSet = ModuleSet()
        self.__file_section: FileSection = FileSection()
        self.__gate_section: GateSection = GateSection()
        self.__pulse_section: PulseSection = PulseSection()
        self.__code_section: CodeSection = CodeSection()
        self.__entry_section: EntrySection = EntrySection()
        self.__layout_section: LayoutSection = LayoutSection()

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def module_set(self) -> ModuleSet:
        return self.__module_set

    @property
    def file_section(self) -> FileSection:
        return self.__file_section

    @property
    def gate_section(self) -> GateSection:
        return self.__gate_section

    @property
    def pulse_section(self) -> PulseSection:
        return self.__pulse_section

    @property
    def code_section(self) -> CodeSection:
        return self.__code_section

    @property
    def entry_section(self) -> EntrySection:
        return self.__entry_section

    @property
    def layout_section(self) -> LayoutSection:
        return self.__layout_section

    def load_module_set(self, module: Module):
        self.__module_set.import_module(module)

    def add_include_file(self, file: File):
        self.__file_section.include_file(file)

    def add_define_gate(self, gate: DefGateConfig):
        # Semantic check about the name legality will be handled in the semantic checker.
        self.__gate_section.define_gate(gate)

    def add_wavecfg(self, wavecfg):
        if isinstance(wavecfg, CustomWaveCfg):
            self.__pulse_section.add_cuswave(wavecfg)
        elif isinstance(wavecfg, DefWaveCfg):
            self.__pulse_section.add_defwave(wavecfg)

    # The work of FuncCall binding with Function is not done yet
    def add_define_function(self, func: Function):
        self.__code_section.def_func(func)

    def add_entry_function(self, func: FuncCall ):
        self.__entry_section.def_entrance_func(func)

    def add_layout_interface(self, interface: Union[PortDeclaration, BindPort]):
        if isinstance(interface, PortDeclaration):
            self.__layout_section.add_port_declaration(interface)
        else:
            self.__layout_section.add_bind_port_insn(interface)

    def __str__(self) -> str:
        return f"{self.module_set}\n{self.file_section}\n{self.gate_section}\n{self.pulse_section}\n{self.code_section}\n{self.entry_section}\n{self.layout_section}"
