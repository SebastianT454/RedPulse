from enum import Enum

# Clase Usuario

class TipoDocumento(Enum):
    CEDULA_CIUDADANIA = "Cedula de Ciudadania"
    CEDULA_EXTRANJERIA = "Cedula de Extranjeria"

class Usuario:
    def __init__(self, nombre: str, correo: str, numero_documento: str, 
                 donante: bool, admin: bool, enfermero: bool, 
                 tipo_documento: TipoDocumento):
        self.nombre = nombre
        self.correo = correo
        self.numero_documento = numero_documento
        self.donante = donante
        self.admin = admin
        self.enfermero = enfermero
        self.tipo_documento = tipo_documento