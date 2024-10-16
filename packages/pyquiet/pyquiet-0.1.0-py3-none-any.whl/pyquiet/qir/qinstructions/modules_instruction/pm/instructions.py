from typing import Union
from pyquiet.qir.qvariable import QuietVariable
from pyquiet.qir.qmodule.modules import Module
from pyquiet.qir.qinstructions.insn_base import InsnBase
from pyquiet.qir.qliteral import Time, Port


###########################################
#           Wave Form Instrucion          #
###########################################
TimePara = Union[Time, QuietVariable]
FloatPara = Union[float, QuietVariable]


class WaveFormInsn(InsnBase):
    def __init__(self, opname: str, duration: TimePara, wave: QuietVariable) -> None:
        super().__init__(opname)
        self.__duration = duration
        self.__wave = wave
        self.__module = Module.pm

    @property
    def module(self):
        return self.__module

    @property
    def duration(self):
        return self.__duration

    @property
    def wave(self):
        return self.__wave


class Square(WaveFormInsn):
    def __init__(self, amp: FloatPara, duration: TimePara, wave: QuietVariable) -> None:
        super().__init__("square", duration, wave)
        self.__amp = amp

    @property
    def amp(self):
        return self.__amp

    def __str__(self):
        return f"square({self.__amp}, {self.duration}) {self.wave}"


class Cos(WaveFormInsn):
    def __init__(
        self,
        amp: FloatPara,
        freq: FloatPara,
        phase: FloatPara,
        duration: TimePara,
        wave: QuietVariable,
    ) -> None:
        super().__init__("cos", duration, wave)
        self.__amp = amp
        self.__freq = freq
        self.__phase = phase

    @property
    def amp(self):
        return self.__amp

    @property
    def freq(self):
        return self.__freq

    @property
    def phase(self):
        return self.__phase

    def __str__(self):
        return f"cos({self.__amp}, {self.__freq}, {self.__phase}, {self.duration}) {self.wave}"


class Sin(WaveFormInsn):
    def __init__(
        self,
        amp: FloatPara,
        freq: FloatPara,
        phase: FloatPara,
        duration: TimePara,
        wave: QuietVariable,
    ) -> None:
        super().__init__("sin", duration, wave)
        self.__amp = amp
        self.__freq = freq
        self.__phase = phase

    @property
    def amp(self):
        return self.__amp

    @property
    def freq(self):
        return self.__freq

    @property
    def phase(self):
        return self.__phase

    def __str__(self):
        return f"sin({self.__amp}, {self.__freq}, {self.__phase}, {self.duration}) {self.wave}"


class Gaussian(WaveFormInsn):
    def __init__(
        self,
        amp: FloatPara,
        mu: FloatPara,
        sigma: FloatPara,
        duration: TimePara,
        wave: QuietVariable,
    ) -> None:
        super().__init__("gaussian", duration, wave)
        self.__amp = amp
        self.__mu = mu
        self.__sigma = sigma

    @property
    def amp(self):
        return self.__amp

    @property
    def mu(self):
        return self.__mu

    @property
    def sigma(self):
        return self.__sigma

    def __str__(self):
        return f"gaussian({self.__amp}, {self.__mu}, {self.__sigma}, {self.duration}) {self.wave}"


class Drag(WaveFormInsn):
    def __init__(
        self,
        g_amp: FloatPara,
        dg_amp: FloatPara,
        phase: FloatPara,
        nr_sigma: FloatPara,
        duration: TimePara,
        wave: QuietVariable,
    ) -> None:
        super().__init__("drag", duration, wave)
        self.__g_amp = g_amp
        self.__dg_amp = dg_amp
        self.__phase = phase
        self.__nr_sigma = nr_sigma

    @property
    def g_amp(self):
        return self.__g_amp

    @property
    def dg_amp(self):
        return self.__dg_amp

    @property
    def phase(self):
        return self.__phase

    @property
    def nr_sigma(self):
        return self.__nr_sigma

    def __str__(self):
        return f"drag({self.__g_amp}, {self.__dg_amp}, {self.__phase}, {self.__nr_sigma}, {self.duration}) {self.wave}"


class Ramp(WaveFormInsn):
    def __init__(
        self, amp: FloatPara, offset: FloatPara, duration: TimePara, wave: QuietVariable
    ) -> None:
        super().__init__("ramp", duration, wave)
        self.__amp = amp
        self.__offset = offset

    @property
    def amp(self):
        return self.__amp

    @property
    def offset(self):
        return self.__offset

    def __str__(self):
        return f"ramp({self.__amp}, {self.__offset}, {self.duration}) {self.wave}"


###########################################
#        Wave Operation Instrucion        #
###########################################
class WaveOpIns(InsnBase):
    def __init__(self, opname: str, wave_dst: QuietVariable) -> None:
        super().__init__(opname)
        self.__wave_dst = wave_dst
        self.__module = Module.pm

    @property
    def module(self):
        return self.__module

    @property
    def wave_dst(self):
        return self.__wave_dst


class Addp(WaveOpIns):
    def __init__(
        self,
        wave_dst: QuietVariable,
        wave_src1: QuietVariable,
        wave_src2: QuietVariable,
    ) -> None:
        super().__init__("addp", wave_dst)
        self.__wave_src1 = wave_src1
        self.__wave_src2 = wave_src2

    @property
    def wave_src1(self):
        return self.__wave_src1

    @property
    def wave_src2(self):
        return self.__wave_src2

    def __str__(self) -> str:
        return f"{self.opname} {self.wave_dst}, {self.__wave_src1}, {self.__wave_src2}"


class Subp(WaveOpIns):
    def __init__(
        self,
        wave_dst: QuietVariable,
        wave_src1: QuietVariable,
        wave_src2: QuietVariable,
    ) -> None:
        super().__init__("subp", wave_dst)
        self.__wave_src1 = wave_src1
        self.__wave_src2 = wave_src2

    @property
    def wave_src1(self):
        return self.__wave_src1

    @property
    def wave_src2(self):
        return self.__wave_src2

    def __str__(self) -> str:
        return f"{self.opname} {self.wave_dst}, {self.__wave_src1}, {self.__wave_src2}"


class Mulp(WaveOpIns):
    def __init__(
        self,
        wave_dst: QuietVariable,
        wave_src1: QuietVariable,
        wave_src2: QuietVariable,
    ) -> None:
        super().__init__("mulp", wave_dst)
        self.__wave_src1 = wave_src1
        self.__wave_src2 = wave_src2

    @property
    def wave_src1(self):
        return self.__wave_src1

    @property
    def wave_src2(self):
        return self.__wave_src2

    def __str__(self) -> str:
        return f"{self.opname} {self.wave_dst}, {self.__wave_src1}, {self.__wave_src2}"


class Convp(WaveOpIns):
    def __init__(
        self,
        wave_dst: QuietVariable,
        wave_src1: QuietVariable,
        wave_src2: QuietVariable,
    ) -> None:
        super().__init__("convp", wave_dst)
        self.__wave_src1 = wave_src1
        self.__wave_src2 = wave_src2

    @property
    def wave_src1(self):
        return self.__wave_src1

    @property
    def wave_src2(self):
        return self.__wave_src2

    def __str__(self) -> str:
        return f"{self.opname} {self.wave_dst}, {self.__wave_src1}, {self.__wave_src2}"


class Joinp(WaveOpIns):
    def __init__(
        self,
        wave_dst: QuietVariable,
        wave_src1: QuietVariable,
        wave_src2: QuietVariable,
    ) -> None:
        super().__init__("joinp", wave_dst)
        self.__wave_src1 = wave_src1
        self.__wave_src2 = wave_src2

    @property
    def wave_src1(self):
        return self.__wave_src1

    @property
    def wave_src2(self):
        return self.__wave_src2

    def __str__(self) -> str:
        return f"{self.opname} {self.wave_dst}, {self.__wave_src1}, {self.__wave_src2}"


class Scalep(WaveOpIns):
    def __init__(
        self,
        wave_dst: QuietVariable,
        wave_src1: QuietVariable,
        wave_src2: QuietVariable,
    ) -> None:
        super().__init__("scalep", wave_dst)
        self.__wave_src1 = wave_src1
        self.__wave_src2 = wave_src2

    @property
    def wave_src1(self):
        return self.__wave_src1

    @property
    def wave_src2(self):
        return self.__wave_src2

    def __str__(self) -> str:
        return f"{self.opname} {self.wave_dst}, {self.__wave_src1}, {self.__wave_src2}"


class Flipp(WaveOpIns):
    def __init__(self, wave_dst: QuietVariable, wave_src: QuietVariable) -> None:
        super().__init__("flipp", wave_dst)
        self.__wave_src = wave_src

    @property
    def wave_src(self):
        return self.__wave_src

    def __str__(self) -> str:
        return f"{self.opname} {self.wave_dst}, {self.__wave_src}"


class Cutp(WaveOpIns):
    def __init__(
        self,
        start_time: Time,
        end_time: Time,
        wave_dst: QuietVariable,
        wave_src: QuietVariable,
    ) -> None:
        super().__init__("cutp", wave_dst)
        self.__start_time = start_time
        self.__end_time = end_time
        self.__wave_src = wave_src

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    @property
    def wave_src(self):
        return self.__wave_src

    def __str__(self) -> str:
        return f"{self.opname}({self.__start_time}, {self.__end_time}) {self.wave_dst}, {self.__wave_src}"


###########################################
#        Port Configure Instrucion        #
###########################################
class PortCfgIns(InsnBase):
    def __init__(self, opname: str, port: Port) -> None:
        super().__init__(opname)
        self.__port = port
        self.__module = Module.pm

    @property
    def module(self):
        return self.__module

    @property
    def port(self):
        return self.__port


class Setfreq(PortCfgIns):
    def __init__(self, port: Port, freq: float) -> None:
        super().__init__("setfreq", port)
        self.__freq = freq

    @property
    def freq(self):
        return self.__freq

    def __str__(self):
        return f"{self.opname} {self.port}, {self.__freq}"


class Setphase(PortCfgIns):
    def __init__(self, port: Port, phase: float) -> None:
        super().__init__("setphase", port)
        self.__phase = phase

    @property
    def phase(self):
        return self.__phase

    def __str__(self):
        return f"{self.opname} {self.port}, {self.__phase}"


class Shiftphase(PortCfgIns):
    def __init__(self, port: Port, phase: float) -> None:
        super().__init__("shiftphase", port)
        self.__phase = phase

    @property
    def phase(self):
        return self.__phase

    def __str__(self):
        return f"{self.opname} {self.port}, {self.__phase}"


###########################################
#           Wave Play Instrucion          #
###########################################
class WavePlayIns(InsnBase):
    def __init__(self, opname: str, port: Port, wave: QuietVariable) -> None:
        super().__init__(opname)
        self.__port = port
        self.__wave = wave
        self.__module = Module.pm

    @property
    def module(self):
        return self.__module

    @property
    def port(self):
        return self.__port

    @property
    def wave(self):
        return self.__wave

    def __str__(self) -> str:
        return f"{self.opname} {self.__port}, {self.__wave}"


class Play(WavePlayIns):
    def __init__(self, port: Port, wave: QuietVariable) -> None:
        super().__init__("play", port, wave)


class Playmod(WavePlayIns):
    def __init__(self, port: Port, wave: QuietVariable) -> None:
        super().__init__("playmod", port, wave)


###########################################
#        Signal Capture Instrucion        #
###########################################
class SignalCapIns(InsnBase):
    def __init__(self, opname: str, port: Port) -> None:
        super().__init__(opname)
        self.__port = port
        self.__module = Module.pm

    @property
    def module(self):
        return self.__module

    @property
    def port(self):
        return self.__port


class CapSignal(SignalCapIns):
    def __init__(self, port: Port) -> None:
        super().__init__("capsignal", port)

    def __str__(self) -> str:
        return f"{self.opname} {self.port}"


class CapBit(SignalCapIns):
    def _init__(self, dst: QuietVariable, port: Port) -> None:
        super().__init__("capbit", port)
        self.__dst = dst

    @property
    def dst(self):
        return self.__dst

    def __str__(self) -> str:
        return f"{self.opname} {self.__dst}, {self.port}"
