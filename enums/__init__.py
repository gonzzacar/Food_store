from enum import Enum

class Rol(Enum):
    ADMIN = "Administrador"
    USUARIO = "Cliente"

class Estado(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"
    TERMINADO = "Terminado"
    CANCELADO = "Cancelado"

class FormaPago(Enum):
    TARJETA = "Tarjeta"
    TRANSFERENCIA = "Transferencia"
    EFECTIVO = "Efectivo"
