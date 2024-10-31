from servicios.usuario_bd_servicio import obtenerUsuarioPorDocumento, actualizarEstadoDonante, agregarPuntos
from servicios.registro_bd_servicio import insertarEnTabla as insertarRegistro
from modelos.registro import Registro, TipoRegistro, TipoSangre

<<<<<<< HEAD
def agregar_donacion(tipo_documento, numero_documento, cantidad_donada, tipo_sangre, razon="Donación", comentarios="", prioridad=5):
=======
def agregar_donacion(tipo_documento, numero_documento, cantidad_donada, tipo_sangre, razon="Donación", comentarios="", prioridad=6):
>>>>>>> 1991f9e0f0edf505af3015b583149403eb8aa27d
    try:
        usuario = obtenerUsuarioPorDocumento(numero_documento)

        if not usuario.donante:
            actualizarEstadoDonante(numero_documento, tipo_documento)

        nuevo_registro = Registro(
            id=None, 
            tipo_registro=TipoRegistro.DONACION,
            tipo_sangre=TipoSangre[tipo_sangre],  
            cantidad=cantidad_donada,
            razon=razon,
            comentarios=comentarios,
            documento_usuario=numero_documento,
            prioridad=prioridad
        )
        
        insertarRegistro(nuevo_registro)
        

        agregarPuntos(numero_documento, tipo_documento, 2000)

    except Exception as e:
        print(f"Ocurrió un error al agregar la donación: {e}")
