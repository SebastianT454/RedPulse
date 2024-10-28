# Controla las operaciones de almacenamiento de la clase usuario

import sys
sys.path.append("src")

# Importando el modelo
from modelos.usuario import Usuario

# Importando librerias para la DB
import psycopg2
import secret_config

class ErrorNotFound( Exception ):
    """ Excepcion que indica que una row buscada no fue encontrada"""
    pass

def obtenerCursor() :
    """
    Crea la conexion a la base de datos y retorna un cursor para ejecutar instrucciones
    """
    DATABASE = secret_config.PGDATABASE
    USER = secret_config.PGUSER
    PASSWORD = secret_config.PGPASSWORD
    HOST = secret_config.PGHOST
    PORT = secret_config.PGPORT

    connection = psycopg2.connect( database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT )
    return connection.cursor()

def crearTabla():
    """
    Crea la tabla de usuarios, en caso de que no exista
    """    
    sql = ""
    with open("sql/crear_usuario.sql","r") as f:
        sql = f.read()

    cursor = obtenerCursor()
    try:
        cursor.execute( sql )
        cursor.connection.commit()
    except:
        # SI LLEGA AQUI, ES PORQUE LA TABLA YA EXISTE
        cursor.connection.rollback()

def borrarTabla():
    """
    Borra (DROP) la tabla en su totalidad
    """    
    sql = "drop table usuarios;"
    cursor = obtenerCursor()
    cursor.execute( sql )
    cursor.connection.commit()

def borrarFilas():
    """
    Borra todas las filas de la tabla (DELETE)
    """
    sql = "delete from usuarios;"
    cursor = obtenerCursor()
    cursor.execute( sql )
    cursor.connection.commit()

def insertarEnTabla( usuario ):
    """ Guarda un usuario en la base de datos """

    cursor = obtenerCursor()

    try:
        # Todas las instrucciones se ejecutan a tavés de un cursor
        cursor.execute(f"""
        insert into usuarios (
            nombre, contrasena, correo, numero_documento, donante, admin, enfermero, tipo_documento
        )
        values 
        (
            '{usuario.nombre}',  '{usuario.contrasena}', '{usuario.correo}', '{usuario.numero_documento}', '{usuario.donante}', '{usuario.admin}', '{usuario.enfermero}', '{usuario.tipo_documento}'
        );
                       """)

        # Las instrucciones DDL y DML no retornan resultados, por eso no necesitan fetchall()
        # pero si necesitan commit() para hacer los cambios persistentes

        cursor.connection.commit()
    except:
        cursor.connection.rollback() 
        raise Exception("No fue posible insertar el usuario con el numero de documento: " + usuario.numero_documento)
    

def obtenerUsuarioPorDocumento( numero_documento ):    
    """ Busca un usuario por el numero de documento y lo retornamos como objeto """

    cursor = obtenerCursor()
    cursor.execute(f"SELECT nombre, contrasena, correo, numero_documento, donante, admin, enfermero, tipo_documento from usuarios where numero_documento = '{numero_documento}' ")
    row = cursor.fetchone()

    if row is None:
        raise ErrorNotFound("El usuario buscado, no fue encontrado. Numero documento: " + str(numero_documento))

    result = Usuario( row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7] )
    return result

def verificarExistenciaUsuario( numero_documento ):
    """ Busca un usuario por el numero de documento y validamos si existe """

    cursor = obtenerCursor()
    cursor.execute(f"SELECT nombre, contrasena, correo, numero_documento, donante, admin, enfermero, tipo_documento from usuarios where numero_documento = '{numero_documento}' ")
    row = cursor.fetchone()

    if row is None:
        return False
    return True

def borrarUsuario( numero_documento ):
    """ Elimina la fila que contiene a un usuario en la BD """

    cursor = obtenerCursor()

    try:
        #Verificamos si el usuario existe
        obtenerUsuarioPorDocumento(numero_documento)

        # Si existe hacer la eliminacion en la tabla.
        sql = f"delete from usuarios where numero_documento = '{numero_documento}'"
        cursor.execute( sql )
        cursor.connection.commit()

    except:
        cursor.connection.rollback()
        raise Exception("No fue posible eliminar el usuario con el numero de documento: " + str(numero_documento))

def actualizarEstadoDonante(numero_documento, tipo_documento):
    cursor = obtenerCursor()
    try:
        sql = f"UPDATE usuarios SET donante = TRUE WHERE numero_documento = '{numero_documento}' AND tipo_documento = '{tipo_documento}'"
        cursor.execute(sql)
        cursor.connection.commit()
    except Exception as e:
        cursor.connection.rollback()
        raise Exception("No fue posible actualizar el estado de donante para el usuario con el numero de documento: " + str(numero_documento)) from e


def agregarPuntos(numero_documento, tipo_documento,cantidad_puntos):
    """ Agrega una cantidad de puntos al usuario especificado """
    
    cursor = obtenerCursor()
    try:
        sql = f"UPDATE usuarios SET puntos = puntos + {cantidad_puntos} WHERE numero_documento = '{numero_documento}' AND tipo_documento = '{tipo_documento}'"
        cursor.execute(sql)
        cursor.connection.commit()
    except Exception as e:
        cursor.connection.rollback()
        raise Exception("No fue posible agregar puntos al usuario con el numero de documento: " + str(numero_documento)) from e