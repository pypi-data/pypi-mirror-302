from typing import Dict, List
from pyquiet.qir.qfile.file import File

class FileSection:
    def __init__(self) -> None:
        self.__file_table: Dict[str, File] = {}

    @property
    def included_files(self) -> List[File]:
        files = [file for file in self.__file_table.values()]
        return files

    def include_file(self, qi_file: File):
        if self.__file_table.get(qi_file.name) == None:
            self.__file_table[qi_file.name] = qi_file

    def get_file(self, file_name: str):
        file = self.__file_table.get(file_name)
        if file == None:
            raise ValueError("The file is not included yet.")
        return file
    
    def __str__(self) -> str:
        if len(self.__file_table) != 0:
            return ".file:""\n\tinclude " + ", ".join(str(filestr) for filestr in self.__file_table.values())
        else:
            return ".file:\n"
    
    def __len__(self) -> str:
        return len(self.__file_table)
