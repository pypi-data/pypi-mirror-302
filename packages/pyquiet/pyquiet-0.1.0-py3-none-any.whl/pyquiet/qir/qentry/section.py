from typing import Dict
from pyquiet.qir.qfunction.function import Function
from pyquiet.qir.qinstructions import FuncCall

class EntrySection:
    def __init__(self) -> None:
        self.__entrance_func : Function = None
        self.__entrance_func_call : FuncCall = None

    @property
    def entrance_function(self) -> Function:
        return self.__entrance_func
    
    @property
    def entrance_function_call(self) -> FuncCall:
        return self.__entrance_func_call

    def def_entrance_func(self, func_call: FuncCall):
        self.__entrance_func_call = func_call
        self.__entrance_func = func_call.function

    def __str__(self) -> str:
        if self.__entrance_func is not None:
            return f".entry:\n{self.__entrance_func_call}"
        else:
            return ".entry:\n"