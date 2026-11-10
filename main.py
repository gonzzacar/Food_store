from entidades import Categoria, Producto, Usuario
from enums import Rol
from servicios import CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio
from consola import crear_menu
from excepciones import FoodStoreError

def main() -> None:
    categorias = CategoriaServicio()
    productos = ProductoServicio(categorias)
    usuarios = UsuarioServicio()
    pedidos = PedidoServicio(usuarios, productos)

    # Datos iniciales para que el sistema pueda probarse inmediatamente.
    categoria = categorias.crear("Hamburguesas", "Hamburguesas y combos")
    categoria_papas = categorias.crear("Acompañamientos", "Papas y guarniciones")
    productos.crear("Hamburguesa clásica", 4500.0, "Carne, lechuga y tomate", 8, "hamburguesa.jpg", True, categoria.id)
    productos.crear("Papas fritas", 1800.0, "Porción mediana", 10, "papas.jpg", True, categoria_papas.id)
    usuarios.crear("Ana", "Pérez", "admin@foodstore.com", "2615550000", "admin123", Rol.ADMIN)
    usuarios.crear("Juan", "Gómez", "cliente@foodstore.com", "2615551111", "cliente123", Rol.USUARIO)

    print("=== FOOD STORE – INICIO DE SESIÓN ===")
    while True:
        usuario = None
        for intento in range(3):
            mail = input("Mail: ").strip()
            contrasenia = input("Contraseña: ")
            try:
                usuario = usuarios.autenticar(mail, contrasenia)
                break
            except FoodStoreError:
                print("Mail o contraseña incorrectos")
        if usuario is None:
            print("Se agotaron los 3 intentos. Programa finalizado.")
            return
        print(f"Bienvenido/a, {usuario.nombre} {usuario.apellido} [{usuario.rol.name}]")
        menu = crear_menu(usuario, categorias, productos, usuarios, pedidos)
        cerrar = menu.mostrar()
        if not cerrar:
            print("Hasta luego.")
            return

if __name__ == "__main__":
    main()
