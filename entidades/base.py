from abc import ABC
from datetime import datetime
from typing import ClassVar

class Base(ABC):
    _siguiente_id: ClassVar[int] = 1

    def __init__(self) -> None:
        self.__id: int = Base._siguiente_id
        Base._siguiente_id += 1
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise ValueError("El estado eliminado debe ser booleano.")
        self.__eliminado = valor

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    def __eq__(self, otro: object) -> bool:
        return isinstance(otro, Base) and self.id == otro.id

    def __hash__(self) -> int:
        return hash(self.id)
