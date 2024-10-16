from enum import Enum


class TimeUnit(Enum):
    s = 0
    ms = 1
    us = 2
    ns = 3
    ps = 4
    fs = 5

class Time:
    def __init__(self, data: float, unit: TimeUnit) -> None:
        self.__data = data
        self.__unit = unit

    @property
    def data(self):
        return self.__data

    @property
    def unit(self):
        return self.__unit

    def __str__(self) -> str:
        return f"{self.__data}{self.__unit.name}"
