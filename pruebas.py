"""Pruebas básicas del modelo y servicios. Ejecutar: python pruebas.py"""
from entidades import Categoria, Producto, Usuario, Pedido
from enums import Rol, FormaPago, Estado
from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio
from excepciones import StockInsuficienteError, DuplicadoError, OperacionNoPermitidaError

def probar(nombre, funcion) -> None:
    try:
        funcion()
        print(f"✔ {nombre}")
    except Exception as e:
        print(f"✘ {nombre}: {type(e).__name__}: {e}")

def caso_modelo() -> None:
    c = Categoria("Bebidas", "Bebidas frías")
    p = Producto("Agua", 1000, "Botella", 3, "agua.jpg", True, c)
    assert p.precio == 1000 and p.stock == 3
def caso_mail_duplicado() -> None:
    s = UsuarioServicio(); s.crear("A", "B", "a@b.com", "123", "clave", Rol.USUARIO)
    try: s.crear("C", "D", "a@b.com", "456", "clave", Rol.USUARIO)
    except DuplicadoError: return
    raise AssertionError("Debió rechazar el mail repetido")
def caso_pedido_y_stock() -> None:
    cs = CategoriaServicio(); c = cs.crear("Comida", "Platos")
    ps = ProductoServicio(cs); p = ps.crear("Tarta", 2500, "Porción", 2, "tarta.jpg", True, c.id)
    us = UsuarioServicio(); u = us.crear("Juan", "Pérez", "j@p.com", "123", "clave", Rol.USUARIO)
    pedidos = PedidoServicio(us, ps); pedido = pedidos.crear(u.id, FormaPago.EFECTIVO, [(p.id, 2)])
    assert pedido.total == 5000 and p.stock == 0
def caso_stock_insuficiente_no_descuenta() -> None:
    cs = CategoriaServicio(); c = cs.crear("Comida", "Platos")
    ps = ProductoServicio(cs); p = ps.crear("Tarta", 2500, "Porción", 1, "tarta.jpg", True, c.id)
    us = UsuarioServicio(); u = us.crear("Juan", "Pérez", "j@p.com", "123", "clave", Rol.USUARIO)
    pedidos = PedidoServicio(us, ps)
    try: pedidos.crear(u.id, FormaPago.EFECTIVO, [(p.id, 2)])
    except StockInsuficienteError: assert p.stock == 1 and len(pedidos.listar()) == 0; return
    raise AssertionError("Debió lanzar StockInsuficienteError")
def caso_transicion_invalida() -> None:
    u = Usuario("Ana", "Pérez", "a@p.com", "123", "clave", Rol.USUARIO)
    p = Pedido(u, FormaPago.EFECTIVO)
    try: p.cambiar_estado(Estado.TERMINADO)
    except OperacionNoPermitidaError: return
    raise AssertionError("Transición inválida aceptada")

if __name__ == "__main__":
    for nombre, fn in [("modelo", caso_modelo), ("mail único", caso_mail_duplicado),
                       ("pedido descuenta stock", caso_pedido_y_stock),
                       ("stock insuficiente no altera datos", caso_stock_insuficiente_no_descuenta),
                       ("transición inválida", caso_transicion_invalida)]:
        probar(nombre, fn)
