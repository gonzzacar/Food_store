from entidades import Pedido
from enums import Estado, FormaPago
from excepciones import EntidadNoEncontradaError, DatoInvalidoError

class PedidoServicio:
    def __init__(self, usuarios: "UsuarioServicio", productos: "ProductoServicio") -> None:
        self._pedidos: list[Pedido] = []; self._usuarios = usuarios; self._productos = productos
    def listar(self) -> list[Pedido]: return [p for p in self._pedidos if not p.eliminado]
    def obtener(self, id_: int) -> Pedido:
        for p in self._pedidos:
            if p.id == id_ and not p.eliminado: return p
        raise EntidadNoEncontradaError("Pedido inexistente o eliminado.")
    def crear(self, usuario_id: int, forma_pago: FormaPago, items: list[tuple[int, int]]) -> Pedido:
        usuario = self._usuarios.obtener(usuario_id)
        pedido = Pedido(usuario, forma_pago)
        # Validar todo primero para que una falta de stock no modifique nada.
        cantidades: dict[int, int] = {}
        for producto_id, cantidad in items:
            producto = self._productos.obtener(producto_id)
            if cantidad <= 0: raise DatoInvalidoError("La cantidad debe ser mayor que cero.")
            cantidades[producto_id] = cantidades.get(producto_id, 0) + cantidad
        for producto_id, cantidad in cantidades.items():
            producto = self._productos.obtener(producto_id)
            if not producto.disponible: raise DatoInvalidoError(f"{producto.nombre} no está disponible.")
            if cantidad > producto.stock:
                from excepciones import StockInsuficienteError
                raise StockInsuficienteError(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}.")
        for producto_id, cantidad in cantidades.items():
            pedido.agregar_detalle(cantidad, self._productos.obtener(producto_id))
        for producto_id, cantidad in cantidades.items():
            p = self._productos.obtener(producto_id); p.stock -= cantidad
        self._pedidos.append(pedido)
        return pedido
    def actualizar(self, id_: int, estado: Estado | None, forma_pago: FormaPago | None) -> Pedido:
        p = self.obtener(id_)
        estado_anterior = p.estado
        if estado is not None: p.cambiar_estado(estado)
        if forma_pago is not None: p.forma_pago = forma_pago
        if estado == Estado.CANCELADO and estado_anterior != Estado.CANCELADO:
            for d in p.detalles: d.producto.stock += d.cantidad
        return p
    def eliminar(self, id_: int) -> None:
        p = self.obtener(id_)
        if p.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            for d in p.detalles: d.producto.stock += d.cantidad
        p.eliminado = True
        for d in p.detalles: d.eliminado = True
    def de_usuario(self, usuario_id: int) -> list[Pedido]:
        return [p for p in self.listar() if p.usuario.id == usuario_id]
