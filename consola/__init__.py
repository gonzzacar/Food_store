from consola.menu import Menu, MenuCliente
from consola.menu_administrador import MenuAdministrador

def crear_menu(usuario, categorias, productos, usuarios, pedidos) -> Menu:
    if usuario.rol.name == "ADMIN":
        return MenuAdministrador(usuario, categorias, productos, usuarios, pedidos)
    return MenuCliente(usuario, categorias, productos, usuarios, pedidos)
