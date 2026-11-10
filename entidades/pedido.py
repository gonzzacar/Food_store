from datetime import date
from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from enums import Estado, FormaPago
from excepciones import DatoInvalidoError, StockInsuficienteError, OperacionNoPermitidaError

class Pedido(Base, Calculable):
    def __init__(self, usuario: "Usuario", forma_pago: FormaPago) -> None:
        super().__init__()
        if usuario.eliminado: raise DatoInvalidoError("No se puede crear un pedido para un usuario eliminado.")
        self.__usuario = usuario
        self.__fecha: date = date.today()
        self.__estado = Estado.PENDIENTE
        self.__forma_pago = forma_pago
        self.__total = 0.0
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> "Usuario": return self.__usuario
    @property
    def fecha(self) -> date: return self.__fecha
    @property
    def estado(self) -> Estado: return self.__estado
    @property
    def forma_pago(self) -> FormaPago: return self.__forma_pago
    @forma_pago.setter
    def forma_pago(self, v: FormaPago) -> None:
        if not isinstance(v, FormaPago): raise DatoInvalidoError("Forma de pago inválida.")
        self.__forma_pago = v
    @property
    def total(self) -> float: return self.__total
    @property
    def detalles(self) -> tuple[DetallePedido, ...]: return tuple(self.__detalles)

    def buscar_detalle_por_producto(self, producto: "Producto") -> DetallePedido | None:
        return next((d for d in self.__detalles if d.producto == producto and not d.eliminado), None)

    def agregar_detalle(self, cantidad: int, producto: "Producto") -> None:
        if self.estado in (Estado.TERMINADO, Estado.CANCELADO):
            raise OperacionNoPermitidaError("No se pueden modificar pedidos cerrados.")
        if producto.eliminado or not producto.disponible:
            raise DatoInvalidoError("El producto no está disponible para nuevos pedidos.")
        detalle = self.buscar_detalle_por_producto(producto)
        cantidad_final = cantidad + (detalle.cantidad if detalle else 0)
        if cantidad <= 0: raise DatoInvalidoError("La cantidad debe ser mayor que cero.")
        if cantidad_final > producto.stock:
            raise StockInsuficienteError(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}.")
        if detalle:
            detalle.aumentar(cantidad)
        else:
            self.__detalles.append(DetallePedido(cantidad, producto))
        self.calcular_total()

    def eliminar_detalle_por_producto(self, producto: "Producto") -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle:
            self.__detalles.remove(detalle)
            self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = sum(d.subtotal for d in self.__detalles if not d.eliminado)

    def cambiar_estado(self, nuevo: Estado) -> None:
        permitidas = {
            Estado.PENDIENTE: {Estado.CONFIRMADO, Estado.CANCELADO},
            Estado.CONFIRMADO: {Estado.TERMINADO, Estado.CANCELADO},
            Estado.TERMINADO: set(), Estado.CANCELADO: set()
        }
        if nuevo == self.__estado: return
        if nuevo not in permitidas[self.__estado]:
            raise OperacionNoPermitidaError(f"Transición inválida: {self.__estado.name} → {nuevo.name}.")
        self.__estado = nuevo

    def __str__(self) -> str:
        return f"Pedido {self.id} | {self.usuario.nombre} {self.usuario.apellido} | {self.estado.name} | {self.forma_pago.name} | ${self.total:.2f} | {self.fecha}"
