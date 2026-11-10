from entidades.base import Base
from excepciones import DatoInvalidoError

class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: "Producto") -> None:
        super().__init__()
        if cantidad <= 0: raise DatoInvalidoError("La cantidad debe ser mayor que cero.")
        self.__cantidad = cantidad
        self.__producto = producto
        self.__subtotal = cantidad * producto.precio

    @property
    def cantidad(self) -> int: return self.__cantidad
    @property
    def producto(self) -> "Producto": return self.__producto
    @property
    def subtotal(self) -> float: return self.__subtotal
    @property
    def eliminado(self) -> bool: return super().eliminado
    @eliminado.setter
    def eliminado(self, valor: bool) -> None: Base.eliminado.fset(self, valor)

    def aumentar(self, cantidad: int) -> None:
        if cantidad <= 0: raise DatoInvalidoError("La cantidad debe ser mayor que cero.")
        self.__cantidad += cantidad
        self.__subtotal = self.__cantidad * self.__producto.precio

    def __str__(self) -> str:
        return f"{self.producto.nombre} x{self.cantidad} = ${self.subtotal:.2f}"
