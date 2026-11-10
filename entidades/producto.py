from entidades.base import Base
from excepciones import DatoInvalidoError, PrecioInvalidoError

class Producto(Base):
    def __init__(self, nombre: str, precio: float, descripcion: str, stock: int,
                 imagen: str, disponible: bool, categoria: "Categoria") -> None:
        super().__init__()
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.categoria = categoria

    @property
    def nombre(self) -> str: return self.__nombre
    @nombre.setter
    def nombre(self, v: str) -> None:
        if not v.strip(): raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = v.strip()

    @property
    def precio(self) -> float: return self.__precio
    @precio.setter
    def precio(self, v: float) -> None:
        if v < 0: raise PrecioInvalidoError("El precio no puede ser negativo.")
        self.__precio = float(v)

    @property
    def descripcion(self) -> str: return self.__descripcion
    @descripcion.setter
    def descripcion(self, v: str) -> None:
        if not v.strip(): raise DatoInvalidoError("La descripción no puede estar vacía.")
        self.__descripcion = v.strip()

    @property
    def stock(self) -> int: return self.__stock
    @stock.setter
    def stock(self, v: int) -> None:
        if not isinstance(v, int) or v < 0: raise DatoInvalidoError("El stock debe ser un entero no negativo.")
        self.__stock = v

    @property
    def imagen(self) -> str: return self.__imagen
    @imagen.setter
    def imagen(self, v: str) -> None:
        if not v.strip(): raise DatoInvalidoError("La imagen no puede estar vacía.")
        self.__imagen = v.strip()

    @property
    def disponible(self) -> bool: return self.__disponible
    @disponible.setter
    def disponible(self, v: bool) -> None:
        if not isinstance(v, bool): raise DatoInvalidoError("Disponibilidad inválida.")
        self.__disponible = v

    @property
    def categoria(self) -> "Categoria": return self.__categoria
    @categoria.setter
    def categoria(self, v: "Categoria") -> None:
        if v.eliminado: raise DatoInvalidoError("La categoría está eliminada.")
        self.__categoria = v

    def __str__(self) -> str:
        return f"ID {self.id} | {self.nombre} | ${self.precio:.2f} | stock={self.stock} | categoría={self.categoria.nombre}"
