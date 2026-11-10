from entidades.base import Base
from enums import Rol
from excepciones import DatoInvalidoError

class Usuario(Base):
    def __init__(self, nombre: str, apellido: str, mail: str, celular: str,
                 contrasenia: str, rol: Rol) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        if not contrasenia: raise DatoInvalidoError("La contraseña no puede estar vacía.")
        self.__contrasenia = contrasenia
        self.rol = rol

    @property
    def nombre(self) -> str: return self.__nombre
    @nombre.setter
    def nombre(self, v: str) -> None:
        if not v.strip(): raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = v.strip()

    @property
    def apellido(self) -> str: return self.__apellido
    @apellido.setter
    def apellido(self, v: str) -> None:
        if not v.strip(): raise DatoInvalidoError("El apellido no puede estar vacío.")
        self.__apellido = v.strip()

    @property
    def mail(self) -> str: return self.__mail
    @mail.setter
    def mail(self, v: str) -> None:
        v = v.strip().lower()
        if not v or "@" not in v or "." not in v: raise DatoInvalidoError("El mail debe tener un formato válido.")
        self.__mail = v

    @property
    def celular(self) -> str: return self.__celular
    @celular.setter
    def celular(self, v: str) -> None:
        if not v.strip(): raise DatoInvalidoError("El celular no puede estar vacío.")
        self.__celular = v.strip()

    @property
    def rol(self) -> Rol: return self.__rol
    @rol.setter
    def rol(self, v: Rol) -> None:
        if not isinstance(v, Rol): raise DatoInvalidoError("Rol inválido.")
        self.__rol = v

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self.__contrasenia == contrasenia

    def __str__(self) -> str:
        return f"ID {self.id} | {self.nombre} {self.apellido} | {self.mail} | {self.rol.name}"
