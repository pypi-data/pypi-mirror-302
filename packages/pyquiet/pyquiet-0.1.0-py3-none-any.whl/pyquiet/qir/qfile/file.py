from pathlib import Path

class File:
    def __init__(self, file:Path) -> None:
        # check the file whther exists first.
        if not file.exists():
            raise FileNotFoundError("The file does not exist.")
        
        # check the suffix of the qi file
        if file.suffix != ".qi":
            raise ValueError("The file is not a qi file.")
        
        self.__file_address:Path = file.absolute()
        self.__file_name:str = self.__file_address.name

    @property
    def address(self) -> Path:
        return self.__file_address
    
    @property
    def name(self) -> str:
        return self.__file_name
    
    def __str__(self) -> str:
        return self.name
