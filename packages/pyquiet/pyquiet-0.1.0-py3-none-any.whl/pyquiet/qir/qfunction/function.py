from typing import List, Dict, Union
from pyquiet.qir.qvariable import QuietVariable
from pyquiet.qir.qinstructions import Label, QiInstruction, VarDecl


class LabelTable:
    def __init__(self) -> None:
        self.__label_index_map: Dict[Label, int] = {}

    @property
    def label_dict(self) -> dict:
        return self.__label_index_map
        
    def update(self, label:Label, index:int):
        self.__label_index_map[label] = index

    def index(self, label:Label) -> int:
        index = self.__label_index_map.get(label)
        if index is None:
            raise ValueError("The label has not been declared.")
        return index
    
#! When the ListElement is needed, it is parsed at the semantic level, 
#! and here the VarTable only adds NonListVariable and ListVariable.
class VarTable:
    def __init__(self) -> None:
        self.__var_table: Dict[str, QuietVariable] = {}

    def add_var(self, var: QuietVariable):
        var_name = var.name
        if self.__var_table.get(var_name) != None:
            raise ValueError("The variable has been already declared.")
        self.__var_table[var_name] = var

    def get_var(self, var_name:str) -> QuietVariable:
        if var_name not in self.__var_table:
            raise ValueError(f"The Variable '{var_name}' has not been declared yet.")
        return self.__var_table[var_name]
    
    @property
    def var_dict(self) -> Dict[str, QuietVariable]:
        return self.__var_table   

class Function:
    def __init__(self):
        self.__func_name: str

        self.__input_args: List[VarDecl] = []
        self.__output_args: List[VarDecl] = []

        self.__func_body: List[Union[QiInstruction, Label]] = []
        self.__var_table = VarTable()
        self.__label_map = LabelTable()
    
    def init_name(self, name:str):
        self.__func_name = name

    def init_input_args(self, input_list:List[VarDecl] = None):
        if input_list is not None and input_list != []:
            for var_decl in input_list:
                arg = var_decl.var[0]
                self.__var_table.add_var(arg)
            self.__input_args = input_list

    def init_output_args(self, output_list:List[VarDecl] = None):
        if output_list is not None and output_list != []:
            for var_decl in output_list:
                arg = var_decl.var[0]
                self.__var_table.add_var(arg)
            self.__output_args = output_list

    @property
    def declaration(self) -> str:
        inputs = ", ".join([str(arg) for arg in self.__input_args])
        if len(self.__output_args) == 0:
            outputs = ""
        else:
            out_args = ", ".join([str(arg) for arg in self.__output_args])
            outputs = f" -> ({out_args})"
        return f"func {self.name}({inputs}){outputs}:"
    
    @property
    def insns(self) -> str:
        body:str = ''
        for insn in self.__func_body:
            if isinstance(insn, Label):
                body += "\n\n\t\t" + str(insn)
            else:
                body += "\n\t\t" + str(insn)
        return body

    @property
    def name(self):
        return self.__func_name
    
    @property
    def inputs(self) -> List[VarDecl]:
        return self.__input_args
    
    @property
    def outputs(self) -> List[VarDecl]:
        return self.__output_args
    
    @property
    def body(self) -> list:
        return self.__func_body

    @property      
    def var_table(self) -> VarTable:
        return self.__var_table
    
    @property
    def label_map(self) -> LabelTable:
        return self.__label_map

    def push_instr(self, instr: Union[QiInstruction, Label]):
        self.__func_body.append(instr)

    def push_var(self, var:QuietVariable):
        self.__var_table.add_var(var)

    def push_label(self, label:Label, index:int):
        self.__label_map.update(label, index)

    def __str__(self) -> str:
        return f"\t{self.declaration}{self.insns}\n\tend"
    