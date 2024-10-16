from typing import Dict
from pyquiet.qir.qpulse.wave_cfg import CustomWaveCfg, DefWaveCfg

class PulseSection:
    def __init__(self) -> None:
        self.__cuswave_dict: Dict[str, CustomWaveCfg] = {}
        self.__defwave_dict: Dict[str, DefWaveCfg] = {}

    @property
    def cuswave_dict(self):
        return self.__cuswave_dict
    
    @property
    def defwave_dict(self):
        return self.__defwave_dict
    
    def add_cuswave(self, cuswave_cfg: CustomWaveCfg):
        wavecfg_name = cuswave_cfg.name
        if wavecfg_name in self.__cuswave_dict:
            raise ValueError("The customwave is redefined.")
        self.__cuswave_dict[wavecfg_name] = cuswave_cfg

    def add_defwave(self, defwave_cfg: DefWaveCfg):
        wavecfg_name = defwave_cfg.name
        if wavecfg_name in self.__cuswave_dict:
            raise ValueError("The defwave is redefined.")
        self.__cuswave_dict[wavecfg_name] = defwave_cfg

    def __str__(self) -> str:
        cuswave_str = "\n\t".join(str(cuswave) for cuswave in self.cuswave_dict.values())
        defwave_str = "\n\t".join(str(defwave) for defwave in self.defwave_dict.values())
        return f".pulse:\n\t{cuswave_str}\n\t{defwave_str}"