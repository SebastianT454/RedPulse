# Controla las operaciones de almacenamiento de la clase registro

import sys
sys.path.append("src")

# Importando el modelo
from modelos.registro import Registro

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
    Crea la tabla de registros, en caso de que no exista
    """    
    sql = ""
    with open("sql/crear_registro.sql","r") as f:
        sql = f.read()

    cursor = obtenerCursor()
    try:
        cursor.execute( sql )
        cursor.connection.commit()
    except:
        # SI LLEGA AQUI, ES PORQUE LA TABLA YA EXISTE
        cursor.connection.rollback()

def insertarEnTabla( registro ):
    """ Guarda un registro en la base de datos """

    cursor = obtenerCursor()

    try:
        # Todas las instrucciones se ejecutan a tavés de un cursor
        cursor.execute("""
        INSERT INTO registros (
            tipo_registro, tipo_sangre, cantidad, razon, comentarios, prioridad, fecha, usuario_documento, usuario_tipo_documento
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            registro.tipo_registro, registro.tipo_sangre, registro.cantidad,
            registro.razon, registro.comentarios, registro.prioridad,
            registro.fecha, registro.usuario_documento, registro.usuario_tipo_documento
        ))

        # Las instrucciones DDL y DML no retornan resultados, por eso no necesitan fetchall()
        # pero si necesitan commit() para hacer los cambios persistentes

        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback() 
        raise Exception("No fue posible insertar el registro." )
    

def obtenerRegistroPorId( registro_id ):    
    """ Busca un registro por el id y lo retornamos como objeto """

    cursor = obtenerCursor()
    cursor.execute(f"SELECT * from registros where id = '{registro_id}' ")
    row = cursor.fetchone()

    if row is None:
        raise ErrorNotFound("El registro buscado, no fue encontrado.")

    result = Registro( registro_id, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8] )
    return result

def verificarExistenciaRegistro( registro_id ):
    """ Busca un registro por su id y validamos si existe """

    cursor = obtenerCursor()
    cursor.execute(f"SELECT * where id = '{registro_id}' ")
    row = cursor.fetchone()

    if row is None:
        return False
    return True

def borrarRegistro( registro_id ):
    """ Elimina la fila que contiene a un registro en la BD """

    cursor = obtenerCursor()

    try:
        #Verificamos si el registro existe
        obtenerRegistroPorId(registro_id)

        # Si existe hacer la eliminacion en la tabla.
        sql = f"delete from registros where id = '{registro_id}'"
        cursor.execute( sql )
        cursor.connection.commit()

    except:
        cursor.connection.rollback()
        raise Exception("No fue posible eliminar el registro.")