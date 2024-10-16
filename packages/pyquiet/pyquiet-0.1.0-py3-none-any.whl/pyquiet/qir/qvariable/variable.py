from enum import Enum
from typing import Union

class QuietType(Enum):
    IntType = 1
    FloatType = 2
    QubitType = 3
    WaveType = 4
    TimeType = 5

    def name(self) -> str:
        if self == QuietType.IntType:
            return "int"
        elif self == QuietType.FloatType:
            return "float"
        elif self == QuietType.QubitType:
            return "qubit"
        elif self == QuietType.WaveType:
            return "wave"
        elif self == QuietType.TimeType:
            return "time"
        else:
            raise Exception("Invalid type")


class Variable:
    def __init__(self, type: QuietType, var_name: str) -> None:
        self.__var_type: QuietType = type
        self.__var_name: str = var_name

    @property
    def name(self) -> str:
        return self.__var_name

    @property
    def type(self) -> QuietType:
        return self.__var_type


class NonListVariable(Variable):
    def __init__(self, type: QuietType, var_name: str) -> None:
        super().__init__(type, var_name)

    def __str__(self) -> str:
        return self.name
    
class PhyQubit(NonListVariable):
    def __init__(self, var_name: str) -> None:
        super().__init__(type, QuietType.QubitType, var_name)

    def __str__(self) -> str:
        return "$" + self.name

class ListVariable(Variable):
    def __init__(
        self, type: QuietType, var_name: str, length: Union[int, str] = None
    ) -> None:
        super().__init__(type, var_name)
        self.__size = length

    @property
    def size(self):
        return self.__size

    # ? Do we need to differentiate between integer dynamic arrays and integer variable-length arrays?

    @property
    def is_fixed_length_list(self):
        return self.__size != None

    def __str__(self) -> str:
        return self.name

    # Instantiate the element of the list only when we need to use it.
    class ListElement(Variable):
        def __init__(
            self,
            type: QuietType,
            var_name: str,
            list_length: Union[int, str],
            index: Union[int, str],
        ) -> None:
            if isinstance(index, int):
                if (
                    list_length is not None
                    and isinstance(list_length, int)
                    and index >= list_length
                ):
                    raise ValueError(
                        "The index of a list element must be within the bounds of the list's length."
                    )
                if index < 0:
                    raise ValueError("Array elements must be non-negative numbers.")
            super().__init__(type, var_name)

            self.__index = index
            self.__list_size = list_length

        @property
        def index(self):
            return self.__index

        @property
        def list_size(self):
            return self.__list_size

        @property
        def name(self) -> str:
            return f"{super().name}[{self.index}]"

        def __str__(self) -> str:
            return f"{super().name}[{self.index}]"

    def var(self, index: int) -> ListElement:
        return ListVariable.ListElement(self.type, self.name, self.__size, index)
