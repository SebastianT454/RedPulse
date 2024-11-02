# Importar metodo para actualizar la sesion del usuario
from servicios.sesion_servicio import actualizarUsuarioSesion

# Importar el metodo para actualizar los puntos en la base de datos.
from servicios.BaseDeDatos.usuario_bd_servicio import actualizarPuntos

# Importando session
from flask import session

def procesarPuntos(puntos_seleccionados: int):
    # Obtener datos y actualizar en la session y base de datos
    user_data = session.get('user_data')
    puntos_usuario = user_data['puntos']
    numero_documento = user_data['numero_documento']
    tipo_de_documento = user_data['tipo_documento']

    # Verificar si el usuario tiene suficientes puntos para realizar la compra
    puntos_restantes = (puntos_usuario - puntos_seleccionados)

    if puntos_restantes >= 0:
        actualizarUsuarioSesion('puntos', puntos_restantes)
        actualizarPuntos(numero_documento, tipo_de_documento, puntos_restantes)

        return True
    return False