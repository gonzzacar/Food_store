from entidades import Categoria
from excepciones import EntidadNoEncontradaError, DuplicadoError, OperacionNoPermitidaError

class CategoriaServicio:
    def __init__(self) -> None: self._categorias: list[Categoria] = []
    def listar(self) -> list[Categoria]: return [c for c in self._categorias if not c.eliminado]
    def obtener(self, id_: int) -> Categoria:
        for c in self._categorias:
            if c.id == id_ and not c.eliminado: return c
        raise EntidadNoEncontradaError("Categoría inexistente o eliminada.")
    def crear(self, nombre: str, descripcion: str) -> Categoria:
        if any(c.nombre.casefold() == nombre.strip().casefold() and not c.eliminado for c in self._categorias):
            raise DuplicadoError("Ya existe una categoría con ese nombre.")
        c = Categoria(nombre, descripcion); self._categorias.append(c); return c
    def editar(self, id_: int, nombre: str, descripcion: str) -> Categoria:
        c = self.obtener(id_)
        if any(x.id != id_ and x.nombre.casefold() == nombre.strip().casefold() and not x.eliminado for x in self._categorias):
            raise DuplicadoError("Ya existe una categoría con ese nombre.")
        c.nombre = nombre; c.descripcion = descripcion; return c
    def eliminar(self, id_: int, productos: "ProductoServicio") -> None:
        c = self.obtener(id_)
        cantidad = sum(1 for p in productos.listar() if p.categoria == c)
        if cantidad: raise OperacionNoPermitidaError(f"No se puede eliminar: tiene {cantidad} producto(s) activo(s).")
        c.eliminado = True
