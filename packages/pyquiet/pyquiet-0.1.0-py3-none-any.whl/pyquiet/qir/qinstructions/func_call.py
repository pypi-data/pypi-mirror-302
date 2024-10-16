from typing import Union, List
from pyquiet.qir.qvariable import QuietVariable
from pyquiet.qir.qinstructions.insn_base import InsnBase
from pyquiet.qir.qliteral import Time
    
class FuncCall(InsnBase):
    def __init__(
            self, 
            func_name:str, 
            input_args:List[Union[QuietVariable, int, float, Time]] = None, 
            output_args:List[QuietVariable] = None
    ) -> None:
        super().__init__(func_name)
        self.__input_args = input_args
        self.__output_args = output_args
        self._func = None

    @property
    def func_name(self) -> str:
        return self.opname
    
    @property
    def input_args(self):
        return self.__input_args
    
    @property
    def output_args(self):
        return self.__output_args
    
    @property
    def function(self):
        return self._func
    
    def bind_function(self, func):
        if self._func is not None:
            raise ValueError("The Function has been already binded.")
        self._func = func
    
    def __str__(self) -> str:
        input:str = ""
        output:str = ""
        if self.__input_args is not None and self.__input_args != []:
            input = ", ".join(str(args) for args in self.__input_args)
        if self.__output_args is not None and  self.__output_args != []:
            output = " -> " + ", ".join(str(args) for args in self.__output_args)
        return f"{self.func_name}({input}){output}"
    
