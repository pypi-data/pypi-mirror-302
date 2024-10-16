from typing import List, Union
from pyquiet.qir.qvariable import QuietVariable
from pyquiet.qir.qinstructions.insn_base import InsnBase
from pyquiet.qir.qliteral import Time
from pyquiet.qir.qmodule.modules import Module


class CusPmInsnBase(InsnBase):
    def __init__(
        self, opname: str, duration: Union[Time, QuietVariable], output: QuietVariable
    ) -> None:
        super().__init__(opname)
        self.__output = output
        self.__wave_cfg = None
        self.__module = Module.pm
        self.__duration = duration

    @property
    def module(self):
        return self.__module

    @property
    def output(self):
        return self.__output

    @property
    def duration(self):
        return self.__duration

    @property
    def wavecfg(self):
        return self.__wave_cfg

    def bind_wavecfg(self, wavecfg):
        if self.__wave_cfg is not None:
            raise ValueError("The WaveCfg has been already binded.")
        self.__wave_cfg = wavecfg


class CusWaveInsn(CusPmInsnBase):
    def __init__(
        self,
        opname: str,
        duration: Union[Time, QuietVariable],
        output: QuietVariable,
    ) -> None:
        super().__init__(opname, duration, output)

    def __str__(self) -> str:
        return f"{self.opname}({self.duration}) {self.output}"


class DefWaveInsn(CusPmInsnBase):
    def __init__(
        self,
        opname: str,
        output: QuietVariable,
        input: List[Union[QuietVariable, int, float, Time]] = None,
    ) -> None:
        super().__init__(opname, output)
        self.__input = input

    @property
    def input(self):
        return self.__input

    def __str__(self) -> str:
        input_str = ""
        if self.__input is not None:
            input_str = ", ".join([str(para) for para in self.__input])
        return f"{self.opname}({input_str}) -> {self.output}"
