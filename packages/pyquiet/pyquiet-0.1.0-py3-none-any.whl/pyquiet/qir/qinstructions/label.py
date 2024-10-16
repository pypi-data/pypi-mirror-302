class Label:
    def __init__(self, name: str) -> None:
        self.__name: str = name

    @property
    def name(self) -> str:
        return self.__name

    def __str__(self) -> str:
        return f"{self.__name}:"
