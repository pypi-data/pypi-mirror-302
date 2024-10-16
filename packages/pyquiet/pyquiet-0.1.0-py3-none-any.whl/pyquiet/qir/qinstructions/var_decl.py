from typing import List
from pyquiet.qir.qvariable import ListVariable, QuietType, QuietVariable


class VarDecl:
    def __init__(self, type: QuietType, var: List[QuietVariable]) -> None:
        self.__type: QuietType = type
        self.__var: List[QuietVariable] = var

    @property
    def type(self) -> QuietType:
        return self.__type

    @property
    def var(self) -> List[QuietVariable]:
        return self.__var

    def __str__(self) -> str:
        var_type = self.__type.name()
        # check if the variable is a list
        if isinstance(self.__var[0], ListVariable):
            size = ""
            if self.__var[0].is_fixed_length_list == True:
                size = self.__var[0].size
            var_type = f"{var_type}[{size}]"
        vars_name = ", ".join(var.name for var in self.__var)
        return f"{var_type} {vars_name}"
