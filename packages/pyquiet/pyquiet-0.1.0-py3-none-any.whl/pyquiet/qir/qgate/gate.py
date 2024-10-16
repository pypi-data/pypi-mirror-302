import math
import numpy as np

def gen_np_square_matrix(matrix: list):
    if 4 ** math.log(len(matrix), 4) != len(matrix) or len(matrix) == 0:
        return np.array(matrix)
    size = int(math.log(len(matrix), 2))
    new_matrix = [matrix[i : i + size] for i in range(0, len(matrix), size)]
    return np.array(new_matrix)

class DefGateConfig:
    def __init__(self, gate_name: str, matrix: list) -> None:
        self.__name = gate_name
        # form the matrix
        if(len(matrix) == 0 or math.log(len(matrix), 4) % 1 != 0):
            raise ValueError("Matrix size must be 4^n and not be equal to 0.")
        self.__matrix = gen_np_square_matrix(matrix)

    @property
    def operation(self) -> str:
        return self.__name

    @property
    def matrix(self) -> list:
        return self.__matrix
    
    def __str__(self) -> str:
        return f"define {self.__name} {self.__matrix.ravel().tolist()}"

