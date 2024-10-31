import secret_config

# Usuario.
from modelos.usuario import *

# Importando la imagen por defecto del usuario.

url = secret_config.DEFAULT_PROFILE_PICTURE

def generar_usuario_sesion(nombre_completo: str, contrasena: str, correo: str, numero_documento: str, 
                donante: bool, admin: bool, enfermero: bool, puntos: int, total_donado: int, 
                tipo_de_sangre: TipoSangre, tipo_documento: TipoDocumento, perfil_imagen_link: str, 
                perfil_imagen_deletehash: str):
    return {
        'nombre_completo': nombre_completo,
        'contrasena': contrasena,
        'correo': correo,
        'numero_documento': numero_documento,
        'donante': donante,
        'admin': admin,
        'enfermero': enfermero,
        'puntos': puntos,
        'total_donado': total_donado,
        'tipo_de_sangre': tipo_de_sangre,
        'tipo_documento': tipo_documento,
        'perfil_imagen_link': perfil_imagen_link,
        'perfil_imagen_deletehash': perfil_imagen_deletehash
        }


def generar_usuario_imagen(imagen, imgur_handler):
    if imagen and imagen.filename:
        image_data = imgur_handler.send_image(imagen)

        # Si no se pudo guardar, colocar la imagen por default
        if not image_data["success"]:
            return secret_config.DEFAULT_PROFILE_PICTURE, ""
        
        # Guardar la imagen exitosa
        perfil_imagen_link = image_data["data"]["link"]
        perfil_imagen_deletehash = image_data["data"]["deletehash"]

        return perfil_imagen_link, perfil_imagen_deletehash
         
    return secret_config.DEFAULT_PROFILE_PICTURE, ""

