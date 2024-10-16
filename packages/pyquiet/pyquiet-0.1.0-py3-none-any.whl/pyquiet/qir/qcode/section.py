from typing import Dict
from pyquiet.qir.qfunction.function import Function

class CodeSection:
    def __init__(self) -> None:
        self.__func_table: Dict[str, Function] = {}
        # The measure operation is pre-defined in quiet-s.
        measure = Function()
        measure.init_name("measure")
        self.def_func(measure)
        reset = Function()
        reset.init_name("reset")
        self.def_func(reset)

    @property
    def functions(self):
        return [func for func in self.__func_table.values()]

    def def_func(self, function: Function):
        if self.__func_table.get(function.name) != None:
            raise ValueError(f"The function {function.name} has been already defined.")
        self.__func_table[function.name] = function

    def get_func(self, func_name: str) -> Function:
        if func_name in self.__func_table.keys():
            return self.__func_table[func_name]
        raise ValueError(f"The function {func_name} has not been defined yet.")
    
    def __str__(self) -> str:
        func_set : str = "\n".join(str(func) for func in self.__func_table.values() if func.name != "measure" and func.name != "reset")
        return f".code:\n{func_set}"

    def __len__(self):
        # The built-in function is pre-defined in quiet-s and not count it.
        return len(self.__func_table) - 2
