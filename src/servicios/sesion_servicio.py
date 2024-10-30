
import secret_config

# Importando la imagen por defecto del usuario.

url = secret_config.DEFAULT_PROFILE_PICTURE

def generar_usuario_sesion(nombre_completo, contrasena, correo, numero_documento, donante, admin, enfermero, tipo_de_sangre, tipo_documento, perfil_imagen_link, perfil_imagen_deletehash):
    return {
        'nombre_completo': nombre_completo,
        'contrasena': contrasena,
        'correo': correo,
        'numero_documento': numero_documento,
        'donante': donante,
        'admin': admin,
        'enfermero': enfermero,
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

