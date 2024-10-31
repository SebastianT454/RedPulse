from enum import Enum

# Clase Registro

class TipoRegistro(Enum):
    DONACION = "Donacion"
    SOLICITUD = "Solicitud"

class TipoSangre(Enum):
    AB_POS = "AB+"
    AB_NEG = "AB-"
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    O_POS = "O+"
    O_NEG = "O-"

class Registro:
    def __init__(self, id: int, tipo_registro: TipoRegistro, 
                 tipo_sangre: TipoSangre, cantidad: float, 
                 razon: str, comentarios: str, 
                 documento_usuario: str, prioridad: int):
        self.id = id
        self.tipo_registro = tipo_registro
        self.tipo_sangre = tipo_sangre
        self.cantidad = cantidad
        self.razon = razon
        self.comentarios = comentarios
        self.documento_usuario = documento_usuario
        self.prioridad = prioridad  # está entre 1 y 5 como el TRIAGE