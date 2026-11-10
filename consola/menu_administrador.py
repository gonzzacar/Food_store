from consola.menu import Menu, leer_int, leer_float, leer_texto, elegir_enum
from enums import Rol, Estado, FormaPago
from excepciones import FoodStoreError

class MenuAdministrador(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE – ADMINISTRADOR ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("\n1. Categorías\n2. Productos\n3. Usuarios\n4. Pedidos\n9. Cerrar sesión\n0. Salir")
            op = input("Seleccione: ").strip()
            acciones = {"1": self.menu_categorias, "2": self.menu_productos, "3": self.menu_usuarios, "4": self.menu_pedidos}
            if op in acciones: self.ejecutar(acciones[op])
            elif op == "9": return True
            elif op == "0": return False
            else: print("Opción inválida.")

    def submenu(self, titulo: str, opciones: str, acciones: dict) -> None:
        while True:
            print(f"\\n--- {titulo} ---\\n{opciones}")
            op = input("Seleccione: ").strip()
            if op == "0": return
            if op in acciones: self.ejecutar(acciones[op])
            else: print("Opción inválida.")

    def menu_categorias(self) -> None:
        self.submenu("CATEGORÍAS", "\n1. Listar\n2. Crear\n3. Editar\n4. Eliminar\n0. Volver",
            {"1": lambda: self.listar("CATEGORÍAS", self._categorias.listar()),
             "2": self.crear_categoria, "3": self.editar_categoria, "4": self.eliminar_categoria})
    def crear_categoria(self) -> None:
        c = self._categorias.crear(leer_texto("Nombre: "), leer_texto("Descripción: "))
        print(f"Categoría creada con ID {c.id}.")
    def editar_categoria(self) -> None:
        self.listar("CATEGORÍAS", self._categorias.listar()); i = leer_int("ID: ")
        c = self._categorias.obtener(i)
        self._categorias.editar(i, leer_texto(f"Nombre [{c.nombre}]: ", c.nombre), leer_texto(f"Descripción [{c.descripcion}]: ", c.descripcion))
        print("Categoría actualizada.")
    def eliminar_categoria(self) -> None:
        i = leer_int("ID: ")
        if input("¿Confirmar? (S/N): ").strip().upper() == "S":
            self._categorias.eliminar(i, self._productos); print("Categoría eliminada.")

    def menu_productos(self) -> None:
        self.submenu("PRODUCTOS", "\n1. Listar\n2. Crear\n3. Editar\n4. Eliminar\n0. Volver",
            {"1": lambda: self.listar("PRODUCTOS", self._productos.listar()), "2": self.crear_producto,
             "3": self.editar_producto, "4": self.eliminar_producto})
    def datos_producto(self, anterior=None):
        if anterior:
            nombre = leer_texto(f"Nombre [{anterior.nombre}]: ", anterior.nombre)
            precio = input(f"Precio [{anterior.precio}]: ").strip(); precio = float(precio) if precio else anterior.precio
            desc = leer_texto(f"Descripción [{anterior.descripcion}]: ", anterior.descripcion)
            stock = input(f"Stock [{anterior.stock}]: ").strip(); stock = int(stock) if stock else anterior.stock
            imagen = leer_texto(f"Imagen [{anterior.imagen}]: ", anterior.imagen)
            disp = input(f"Disponible S/N [{('S' if anterior.disponible else 'N')}]: ").strip().upper()
            disponible = anterior.disponible if not disp else disp == "S"
            cat = input(f"ID categoría [{anterior.categoria.id}]: ").strip(); cat = int(cat) if cat else anterior.categoria.id
        else:
            nombre = leer_texto("Nombre: "); precio = leer_float("Precio: "); desc = leer_texto("Descripción: ")
            stock = leer_int("Stock: "); imagen = leer_texto("Imagen: ")
            disponible = input("Disponible (S/N): ").strip().upper() == "S"; cat = leer_int("ID categoría: ")
        return nombre, precio, desc, stock, imagen, disponible, cat
    def crear_producto(self) -> None:
        self.listar("CATEGORÍAS", self._categorias.listar())
        p = self._productos.crear(*self.datos_producto()); print(f"Producto creado con ID {p.id}.")
    def editar_producto(self) -> None:
        self.listar("PRODUCTOS", self._productos.listar()); i = leer_int("ID: "); p = self._productos.obtener(i)
        self._productos.editar(i, *self.datos_producto(p)); print("Producto actualizado.")
    def eliminar_producto(self) -> None:
        i = leer_int("ID: ")
        if input("¿Confirmar? (S/N): ").strip().upper() == "S": self._productos.eliminar(i); print("Producto eliminado.")

    def menu_usuarios(self) -> None:
        self.submenu("USUARIOS", "\n1. Listar\n2. Crear\n3. Editar\n4. Eliminar\n0. Volver",
            {"1": lambda: self.listar("USUARIOS", self._usuarios.listar()), "2": self.crear_usuario,
             "3": self.editar_usuario, "4": self.eliminar_usuario})
    def crear_usuario(self) -> None:
        u = self._usuarios.crear(leer_texto("Nombre: "), leer_texto("Apellido: "), leer_texto("Mail: "),
            leer_texto("Celular: "), leer_texto("Contraseña: "), elegir_enum(Rol, "Rol: "))
        print(f"Usuario creado con ID {u.id}.")
    def editar_usuario(self) -> None:
        self.listar("USUARIOS", self._usuarios.listar()); i = leer_int("ID: "); u = self._usuarios.obtener(i)
        self._usuarios.editar(i, leer_texto(f"Nombre [{u.nombre}]: ", u.nombre), leer_texto(f"Apellido [{u.apellido}]: ", u.apellido),
            leer_texto(f"Mail [{u.mail}]: ", u.mail), leer_texto(f"Celular [{u.celular}]: ", u.celular), elegir_enum(Rol, "Nuevo rol: "))
        print("Usuario actualizado.")
    def eliminar_usuario(self) -> None:
        i = leer_int("ID: ")
        if input("¿Confirmar? (S/N): ").strip().upper() == "S": self._usuarios.eliminar(i, self._usuario); print("Usuario eliminado.")

    def menu_pedidos(self) -> None:
        self.submenu("PEDIDOS", "\n1. Listar\n2. Crear pedido\n3. Actualizar estado/pago\n4. Eliminar\n0. Volver",
            {"1": lambda: self.listar("PEDIDOS", self._pedidos.listar()), "2": self.crear_pedido,
             "3": self.actualizar_pedido, "4": self.eliminar_pedido})
    def crear_pedido(self) -> None:
        self.listar("USUARIOS", self._usuarios.listar()); usuario_id = leer_int("ID usuario: ")
        pago = elegir_enum(FormaPago, "Forma de pago: ")
        items = []
        while True:
            self.listar("PRODUCTOS", self._productos.listar(True))
            pid = leer_int("ID producto (0 termina): ")
            if pid == 0: break
            cantidad = leer_int("Cantidad: "); items.append((pid, cantidad))
        if not items: print("Pedido cancelado: debe agregar al menos un producto."); return
        p = self._pedidos.crear(usuario_id, pago, items)
        print(f"Pedido creado: ID {p.id}, total ${p.total:.2f}.")
    def actualizar_pedido(self) -> None:
        self.listar("PEDIDOS", self._pedidos.listar()); i = leer_int("ID: ")
        estado = elegir_enum(Estado, "Estado nuevo (actual): ") 
        pago = elegir_enum(FormaPago, "Forma de pago nueva: ")
        p = self._pedidos.actualizar(i, estado, pago); print(f"Pedido actualizado: {p}")
    def eliminar_pedido(self) -> None:
        i = leer_int("ID: ")
        if input("¿Confirmar? (S/N): ").strip().upper() == "S": self._pedidos.eliminar(i); print("Pedido eliminado.")
