#////////////////////////////// Importaciones //////////////////////////////////////////////
import sys
sys.path.append("src")

from servicios.BaseDeDatos.usuario_bd_servicio import obtenerUsuarioPorDocumento, actualizarEstadoDonante, actualizarPuntos
from servicios.BaseDeDatos.registro_bd_servicio import insertarEnTabla as insertarRegistro, actualizarEstadoRegistro
from modelos.registro import Registro
from datetime import datetime

# Importando session
from flask import session

def insertarDonacion(numero_documento, tipo_documento, fecha, cantidad_donada, tipo_registro="Donacion"):
    try:
        usuario = obtenerUsuarioPorDocumento(numero_documento, tipo_documento)

        if not usuario.donante:
            actualizarEstadoDonante(numero_documento, tipo_documento)

        nuevo_registro = Registro(
            id_registro=None, 
            tipo_registro=tipo_registro,
            tipo_sangre=usuario.tipo_de_sangre,  
            cantidad=cantidad_donada,
            razon=None,
            comentarios=None,
            prioridad=None,
            estado=None,
            fecha = fecha,
            usuario_documento=numero_documento,
            usuario_tipo_documento=tipo_documento
        )
        
        insertarRegistro(nuevo_registro)
        
        actualizarPuntos(numero_documento, tipo_documento, usuario.puntos + 2000)

        return True

    except Exception as e:
        print(f"Ocurrió un error al agregar la donación: {e}")
        return False
    
# Obtener los datos del request HTTP y crear un registro
def crearRegistro(request, user_data):
    tipo_registro = 'Solicitud'
    tipo_sangre = user_data['tipo_de_sangre']
    cantidad = request.form.get('cantidad_sangre_donada')
    razon = request.form.get('razon')
    comentarios = request.form.get('comentarios')
    prioridad = request.form.get('prioridad_solicitud')
    estado = "Pendiente"
    fecha = datetime.now().strftime("%Y-%m-%d")
    usuario_documento = user_data['numero_documento']
    usuario_tipo_documento = user_data['tipo_documento']

    # Crear el registro.
    registro = Registro(None, tipo_registro, tipo_sangre, cantidad, razon, comentarios, prioridad, estado, fecha, usuario_documento, usuario_tipo_documento)

    try:
        # Intentar insertar en la base de datos
        insertarRegistro(registro)
        return True 
    except:
        return False 