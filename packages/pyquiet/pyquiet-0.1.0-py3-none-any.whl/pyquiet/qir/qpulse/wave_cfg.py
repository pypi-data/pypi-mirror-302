from typing import List
from pyquiet.qir.qfunction import VarTable
from pyquiet.qir.qvariable import QuietVariable
from pyquiet.qir.qinstructions import QiInstruction, VarDecl

class CustomWaveCfg:
    def __init__(
        self,
        name: str,
        sampling_rate: int,
        para_list
    ) -> None:
        self.__name = name
        self.__sampling_rate = sampling_rate 
        self.__waveform = para_list

    @property
    def name(self):
        return self.__name

    @property
    def sampling_rate(self):
        return self.__sampling_rate
    
    @property
    def waveform(self):
        return self.__waveform
    
    def __str__(self) -> str:
        waveform = ", ".join(f"({number.real}, {number.imag})" for number in self.__waveform)
        return f"customwave {self.__sampling_rate}, [{waveform}]"

class DefWaveCfg:
    def __init__(self):
        self.__name: str

        self.__input_args: List[VarDecl] = []
        self.__output: VarDecl = None

        self.__func_body: List[QiInstruction] = []
        self.__var_table = VarTable()
    
    def init_name(self, name:str):
        self.__name = name

    def init_input_args(self, input_list:List[VarDecl] = None):
        if input_list is not None and input_list != []:
            for var_decl in input_list:
                arg = var_decl.var[0]
                self.__var_table.add_var(arg)
            self.__input_args = input_list

    def init_output(self, output: VarDecl):
        if self.__output is not None:
            raise ValueError("Output is already inited.")
        self.__var_table.add_var(output.var[0])
        self.__output = output

    @property
    def declaration(self) -> str:
        inputs = ", ".join([str(arg) for arg in self.__input_args])
        outputs = f" -> {str(self.__output)}"
        return f"func {self.name}({inputs}){outputs}:"
    
    @property
    def insns(self) -> str:
        body:str = ''
        for insn in self.__func_body:
            body += "\n\t\t" + str(insn)
        return body

    @property
    def name(self):
        return self.__name
    
    @property
    def inputs(self) -> List[VarDecl]:
        return self.__input_args
    
    @property
    def output(self) -> VarDecl:
        return self.__output
    
    @property
    def body(self) -> list:
        return self.__func_body

    @property      
    def var_table(self) -> VarTable:
        return self.__var_table

    def push_instr(self, instr: QiInstruction):
        self.__func_body.append(instr)

    def push_var(self, var:QuietVariable):
        self.__var_table.add_var(var)

    def __str__(self) -> str:
        return f"\t{self.declaration}{self.insns}\n\tend"
    
