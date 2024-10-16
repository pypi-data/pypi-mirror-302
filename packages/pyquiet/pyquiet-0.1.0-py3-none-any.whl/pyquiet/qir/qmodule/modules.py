from typing import Set
from enum import Enum

class Module(Enum):
    std = 1
    ct = 2
    im = 3
    fm = 4
    pm = 5
    tm = 6

class ModuleSet:
    def __init__(self):
        self.__module_table: Set[Module] = {Module.std} 

    @property
    def modules(self) -> Set[Module]:
        return self.__module_table
        
    def is_imported(self, module : Module) -> bool:
        is_imported = False
        if module in self.__module_table:
            is_imported = True
        return is_imported
            
    def import_module(self, module: Module) -> None:
        self.__module_table.add(module)
        if module == Module.fm or module == Module.im:
            self.__module_table.add(Module.ct)
    # We agree that when 'im' or 'fm' is introduced in the '.qi' file,
    # the 'ct' module will be automatically introduced by default
  
    def __str__(self) -> str:
        return "using " + ", ".join(str(module.name) for module in sorted(self.__module_table, key=lambda x: x.name))
    # Ensure the orderliness of the output
    
    def __len__(self) -> str:
        return len(self.__module_table)