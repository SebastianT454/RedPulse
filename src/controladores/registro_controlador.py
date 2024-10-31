#////////////////////////////// Importaciones //////////////////////////////////////////////
import sys
sys.path.append("src")

# Registro.
from modelos.registro import *

# Base de datos.
from servicios.registro_bd_servicio import *

def crearRegistro(id_registro: int, tipo_registro: TipoRegistro, tipo_sangre: TipoSangre, cantidad: int, 
              razon: str, comentarios: str, prioridad: int, fecha: str, usuario_documento: str, usuario_tipo_documento: str):
    
    # Crear el registro.
    registro = Registro(id_registro, tipo_registro, tipo_sangre, cantidad, razon, comentarios, prioridad, fecha, usuario_documento, usuario_tipo_documento)

    try:
        # Intentar insertar en la base de datos
        insertarEnTabla(registro)
        return True 
    except:
        return False  