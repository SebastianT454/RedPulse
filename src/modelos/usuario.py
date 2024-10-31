<<<<<<< HEAD
from enum import Enum

# Clase Usuario

class TipoDocumento(Enum):
    CEDULA_CIUDADANIA = "Cedula de Ciudadania"
    CEDULA_EXTRANJERIA = "Cedula de Extranjeria"

class TipoSangre(Enum):
    A_POSITIVO = "A+"
    A_NEGATIVO = "A-"
    B_POSITIVO = "B+"
    B_NEGATIVO = "B-"
    AB_POSITIVO = "AB+"
    AB_NEGATIVO = "AB-"
    O_POSITIVO = "O+"
    O_NEGATIVO = "O-"

class Usuario:
    def __init__(self, nombre: str, contrasena: str, correo: str, numero_documento: str, 
                 donante: bool, admin: bool, enfermero: bool, tipo_de_sangre: TipoSangre,
                 tipo_documento: TipoDocumento, perfil_imagen_link: str, perfil_imagen_deletehash: str):
        self.nombre = nombre
        self.contrasena = contrasena
        self.correo = correo
        self.numero_documento = numero_documento
        self.donante = donante
        self.admin = admin
        self.enfermero = enfermero
        self.tipo_de_sangre = tipo_de_sangre
        self.tipo_documento = tipo_documento
        self.perfil_imagen_link = perfil_imagen_link
        self.perfil_imagen_deletehash = perfil_imagen_deletehash
=======
from enum import Enum

# Clase Usuario

class TipoDocumento(Enum):
    CEDULA_CIUDADANIA = "Cedula de Ciudadania"
    CEDULA_EXTRANJERIA = "Cedula de Extranjeria"

class Usuario:
    def __init__(self, nombre: str, contrasena: str, correo: str, numero_documento: str, 
                 donante: bool, admin: bool, enfermero: bool, 
                 tipo_documento: TipoDocumento):
        self.nombre = nombre
        self.contrasena = contrasena
        self.correo = correo
        self.numero_documento = numero_documento
        self.donante = donante
        self.admin = admin
        self.enfermero = enfermero
        self.tipo_documento = tipo_documento
>>>>>>> 1991f9e0f0edf505af3015b583149403eb8aa27d
