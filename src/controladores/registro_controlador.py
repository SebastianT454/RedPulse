#////////////////////////////// Importaciones //////////////////////////////////////////////
import sys
sys.path.append("src")

# Registro.
from modelos.registro import *

# Base de datos.
from servicios.BaseDeDatos.registro_bd_servicio import *

from datetime import datetime

def crearRegistro(request, user_data):
    tipo_registro = 'Solicitud'
    tipo_sangre = user_data['tipo_de_sangre']
    cantidad = request.form.get('cantidad_sangre_donada')
    razon = request.form.get('razon')
    comentarios = request.form.get('comentarios')
    prioridad = request.form.get('prioridad_solicitud')
    fecha = datetime.now().strftime("%Y-%m-%d")
    usuario_documento = user_data['numero_documento']
    usuario_tipo_documento = user_data['tipo_documento']

    # Crear el registro.
    registro = Registro(None, tipo_registro, tipo_sangre, cantidad, razon, comentarios, prioridad, fecha, usuario_documento, usuario_tipo_documento)

    try:
        # Intentar insertar en la base de datos
        insertarEnTabla(registro)
        return True 
    except:
        return False  