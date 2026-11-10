from entidades import Usuario
from enums import Rol
from excepciones import EntidadNoEncontradaError, DuplicadoError, CredencialesInvalidasError, OperacionNoPermitidaError

class UsuarioServicio:
    def __init__(self) -> None: self._usuarios: list[Usuario] = []
    def listar(self) -> list[Usuario]: return [u for u in self._usuarios if not u.eliminado]
    def obtener(self, id_: int) -> Usuario:
        for u in self._usuarios:
            if u.id == id_ and not u.eliminado: return u
        raise EntidadNoEncontradaError("Usuario inexistente o eliminado.")
    def crear(self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol) -> Usuario:
        if any(u.mail == mail.strip().lower() for u in self._usuarios):
            raise DuplicadoError("Ya existe un usuario con ese mail.")
        u = Usuario(nombre, apellido, mail, celular, contrasenia, rol); self._usuarios.append(u); return u
    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        for u in self._usuarios:
            if u.mail == mail.strip().lower() and not u.eliminado and u.verificar_contrasenia(contrasenia):
                return u
        raise CredencialesInvalidasError("Mail o contraseña incorrectos.")
    def editar(self, id_: int, nombre: str, apellido: str, mail: str, celular: str, rol: Rol) -> Usuario:
        u = self.obtener(id_)
        if any(x.id != id_ and x.mail == mail.strip().lower() for x in self._usuarios):
            raise DuplicadoError("Ya existe un usuario con ese mail.")
        u.nombre = nombre; u.apellido = apellido; u.mail = mail; u.celular = celular; u.rol = rol
        return u
    def eliminar(self, id_: int, sesion: Usuario) -> None:
        u = self.obtener(id_)
        if u == sesion and u.rol == Rol.ADMIN: raise OperacionNoPermitidaError("No puede eliminarse a sí mismo con la sesión iniciada.")
        u.eliminado = True
