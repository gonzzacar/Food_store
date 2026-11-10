from abc import ABC, abstractmethod
from entidades import Usuario
from enums import Rol
from excepciones import FoodStoreError
from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio

def leer_int(mensaje: str) -> int:
    while True:
        try: return int(input(mensaje))
        except ValueError: print("Ingrese un número entero válido.")

def leer_float(mensaje: str) -> float:
    while True:
        try: return float(input(mensaje))
        except ValueError: print("Ingrese un número válido.")

def leer_texto(mensaje: str, anterior: str | None = None) -> str:
    v = input(mensaje).strip()
    return v if v else (anterior if anterior is not None else v)

def elegir_enum(tipo: type, mensaje: str):
    valores = list(tipo)
    for i, v in enumerate(valores, 1): print(f"{i}. {v.name} ({v.value})")
    while True:
        n = leer_int(mensaje)
        if 1 <= n <= len(valores): return valores[n-1]
        print("Opción fuera de rango.")

class Menu(ABC):
    def __init__(self, usuario: Usuario, categorias: CategoriaServicio, productos: ProductoServicio,
                 usuarios: UsuarioServicio, pedidos: PedidoServicio) -> None:
        self._usuario = usuario; self._categorias = categorias; self._productos = productos
        self._usuarios = usuarios; self._pedidos = pedidos
    @abstractmethod
    def mostrar(self) -> bool:
        """True cierra sesión; False termina el programa."""
        raise NotImplementedError
    def ejecutar(self, accion) -> None:
        try: accion()
        except (FoodStoreError, ValueError) as e: print(f"Error: {e}")
    def listar(self, titulo: str, objetos: list) -> None:
        print(f"--- {titulo} ---")
        if not objetos: print("No hay elementos cargados.")
        for x in objetos: print(x)
    def categorias_consulta(self) -> None: self.listar("CATEGORÍAS", self._categorias.listar())
    def productos_consulta(self, disponibles: bool = False) -> None:
        self.listar("PRODUCTOS", self._productos.listar(disponibles))
    def mis_datos(self) -> None:
        u = self._usuario
        print(f"{u.nombre} {u.apellido} | {u.mail} | {u.celular} | {u.rol.name}")
    def mis_pedidos(self) -> None:
        pedidos = self._pedidos.de_usuario(self._usuario.id)
        self.listar("MIS PEDIDOS", pedidos)
        if pedidos:
            id_ = leer_int("ID del pedido para ver detalles (0 vuelve): ")
            if id_:
                p = next((x for x in pedidos if x.id == id_), None)
                if p is None: print("Pedido inexistente.")
                else:
                    for d in p.detalles: print(d)
                    print(f"Total: ${p.total:.2f}")

class MenuCliente(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE – CLIENTE ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("\n1. Ver categorías\n2. Ver productos disponibles\n3. Mis pedidos\n4. Mis datos\n9. Cerrar sesión\n0. Salir")
            op = input("Seleccione: ").strip()
            if op == "1": self.ejecutar(self.categorias_consulta)
            elif op == "2": self.ejecutar(lambda: self.productos_consulta(True))
            elif op == "3": self.ejecutar(self.mis_pedidos)
            elif op == "4": self.ejecutar(self.mis_datos)
            elif op == "9": return True
            elif op == "0": return False
            else: print("Opción inválida.")
