#////////////////////////////// Importaciones //////////////////////////////////////////////
import sys
sys.path.append("src")

# Encriptacion.
from werkzeug.security import generate_password_hash, check_password_hash
# generate_password_hash: genera la encriptacion.
# check_password_hash: comprueba si un valor cifrado concuerda con su valor original.

# Base de datos.
from servicios.usuario_bd_servicio import *

# Usuario.
from modelos.usuario import *

#////////////////////////////// Funcionalidades //////////////////////////////////////////////

def verificacionLogin(numero_documento, contrasena):
    # Lógica para iniciar sesión.

    if not verificarUsuario(numero_documento):
        return False
    
    # Obtener el usuario de la base de datos.
    usuario = obtenerUsuarioPorDocumento(numero_documento)

    if not check_password_hash(usuario.contrasena, contrasena):
        return False
    
    return True


def registrarUsuario(nombre: str, contrasena: str, correo: str, numero_documento: str, 
                donante: bool, admin: bool, enfermero: bool, 
                tipo_documento: TipoDocumento):
    # Lógica para registrar un nuevo usuario

    # Encriptar contraseña.
    contrasena_encriptada = generate_password_hash(contrasena, 'pbkdf2:sha256', 10)

    # Crear el usuario ya que no existe.
    usuario = Usuario(nombre, contrasena_encriptada, correo, numero_documento, donante, admin, enfermero, tipo_documento)
    insertarEnTabla(usuario)

def verificarUsuario(numero_documento: str):
    # Verificar si el usuario existen en la db
    usuario_existe = verificarExistenciaUsuario(numero_documento)

    if usuario_existe:
        return True
    return False

#registro("Juan Esteban", "123", "dsad@gmail.com", "12330231", False, False, False, 'Cedula de Ciudadania')