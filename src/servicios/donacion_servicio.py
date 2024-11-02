#////////////////////////////// Importaciones //////////////////////////////////////////////
from servicios.BaseDeDatos.usuario_bd_servicio import obtenerUsuarioPorDocumento, actualizarEstadoDonante, actualizarPuntos
from servicios.BaseDeDatos.registro_bd_servicio import insertarEnTabla as insertarRegistro
from modelos.registro import Registro, TipoRegistro

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
    