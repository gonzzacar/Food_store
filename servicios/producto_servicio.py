from entidades import Producto
from excepciones import EntidadNoEncontradaError, DuplicadoError

class ProductoServicio:
    def __init__(self, categorias: "CategoriaServicio") -> None:
        self._productos: list[Producto] = []; self._categorias = categorias
    def listar(self, solo_disponibles: bool = False) -> list[Producto]:
        return [p for p in self._productos if not p.eliminado and (not solo_disponibles or (p.disponible and p.stock > 0))]
    def obtener(self, id_: int) -> Producto:
        for p in self._productos:
            if p.id == id_ and not p.eliminado: return p
        raise EntidadNoEncontradaError("Producto inexistente o eliminado.")
    def crear(self, nombre: str, precio: float, descripcion: str, stock: int, imagen: str, disponible: bool, categoria_id: int) -> Producto:
        categoria = self._categorias.obtener(categoria_id)
        p = Producto(nombre, precio, descripcion, stock, imagen, disponible, categoria)
        self._productos.append(p); return p
    def editar(self, id_: int, nombre: str, precio: float, descripcion: str, stock: int, imagen: str, disponible: bool, categoria_id: int) -> Producto:
        p = self.obtener(id_); p.nombre = nombre; p.precio = precio; p.descripcion = descripcion
        p.stock = stock; p.imagen = imagen; p.disponible = disponible; p.categoria = self._categorias.obtener(categoria_id)
        return p
    def eliminar(self, id_: int) -> None: self.obtener(id_).eliminado = True
