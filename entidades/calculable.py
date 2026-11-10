from abc import ABC, abstractmethod

class Calculable(ABC):
    @abstractmethod
    def calcular_total(self) -> None:
        """Actualiza el total del objeto."""
        raise NotImplementedError
