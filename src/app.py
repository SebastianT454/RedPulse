#////////////////////////////// Importaciones //////////////////////////////////////////////
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

#Imgur
from servicios.Misc.flask_imgur_servicio import *

#Misc
import os

# Controlador para el login y registro
from controladores.aunteticacion_controlador import *

# Controlador para el registro
from controladores.registro_controlador import *

# Controlador de puntos
from controladores.puntos_controlador import *

# Base de datos, chatbot.
from servicios.BaseDeDatos.usuario_bd_servicio import *
from servicios.chatbot_servicio import *

# Importar el servicio de sesiones construido.
from servicios.sesion_servicio import *

# Importar el servicio de donaciones.
from servicios.donacion_servicio import *

# app principal del Flask
app = Flask(__name__,
            static_url_path='', 
            static_folder= os.path.join(os.path.pardir, 'static'),
            template_folder= os.path.join(os.path.pardir, 'templates'))

# Secreto para el App de Flask
app.secret_key = secret_config.SECRET_KEY_FLASK

# Imgur client id para la API
app.config["IMGUR_ID"] = secret_config.IMGUR_CLIENT_ID
imgur_handler = Imgur(app)

#////////////////////////////// Rutas //////////////////////////////////////////////

@app.route('/estadisticas')
def estadisticas():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')
    
    # Verificar si el usuario ha iniciado sesión
    if not user_data and user_data.get('admin'):
        return render_template('home.html')

    return render_template('estadisticas.html')

# Home, Logout y retorno al home

@app.route('/')
def home():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')
    
    # Verificar si el usuario ha iniciado sesión
    if not user_data:
        return render_template('home.html')

    # Verificar si es admin o enfermero y renderizar el template adecuado
    if user_data.get('admin'):
        return redirect(url_for('estadisticas'))
    elif user_data.get('enfermero'):
        return redirect(url_for('enfermero'))
    else:
        # Se renderiza el home para cada uno.
        return render_template('home.html', user_data=user_data)

@app.route('/logout')
def logout():
    session.clear()  # Eliminar todos los datos de la sesión
    return redirect(url_for('home'))

@app.route('/return_home')
def return_home():
    session['registarse_verificacion_resultado'] = None
    session['login_verificacion_resultado'] = None
    return redirect(url_for('home'))

# Rutas de acceso para un usuario registrado

@app.route('/perfil')
def perfil():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')

    # Verificar si ya hay datos de usuario en la sesión
    if not user_data:
       return redirect(url_for('home'))
    
    return render_template('perfil.html', user_data=user_data)

@app.route('/puntos', methods=['GET', 'POST'])
def puntos():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')

    # Verificar si ya hay datos de usuario en la sesión
    if not user_data:
       return redirect(url_for('home'))
    
    # Obtener los puntos seleccionados
    if request.method == 'POST':
        data = request.get_json()  # Obtener los datos JSON enviados
        puntos_seleccionados = int(data.get('puntos_seleccionados'))  # Acceder a los puntos seleccionados especificamente

        puntos_procesados = procesarPuntos(puntos_seleccionados)
        return jsonify(success=puntos_procesados, nuevos_puntos=obtenerValorUsuarioSesion('puntos'))

    return render_template('puntos.html', user_data=user_data)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')

    # Verificar si ya hay datos de usuario en la sesión
    if not user_data:
       return redirect(url_for('home'))

    if request.method == 'POST':
        data = request.get_json()
        usuario_mensaje_ingresado = data.get("mensaje_ingresado")
        respuesta = generate_response(usuario_mensaje_ingresado)
        return jsonify(respuesta=respuesta)
    
    return render_template('chatBot.html')

@app.route('/solicitud_donacion', methods=['GET', 'POST'])
def solicitud_donacion():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')

    # Verificar si ya hay datos de usuario en la sesión
    if not user_data:
       return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Crear el registro en el sistema.
        registro = crearRegistro(request, user_data)

        # Almacenar el resultado de la operacion
        session['registro_creado'] = registro

    return render_template('solicitud_donacion.html', user_data=user_data)

# Rutas para el enfermero

@app.route('/enfermero', methods=['GET', 'POST'])
def enfermero():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')
    
    # Verificar si el usuario ha iniciado sesión
    if not user_data and user_data.get('enfermero'):
        return render_template('home.html')

    if request.method == 'POST':
        cedula_ingresada = request.form.get('cedula')
        tipo_de_cedula_ingresada = request.form.get('tipo_documento')

        # Verificar si la cuenta ya existe
        exists = verificarExistenciaUsuario(cedula_ingresada, tipo_de_cedula_ingresada)

        # Almacenar el resultado de la verificación en la sesión
        session['enfermero_usuario_verificacion'] = exists

        # Limpiar las sesiones para repetir el proceso
        if 'enfermero_usuario_obtenido' in session:
            session['enfermero_usuario_obtenido'] = None

        if 'donacion_exitosa' in session:
            session['donacion_exitosa'] = None

        if exists:
            session['enfermero_usuario_obtenido'] = {
                'cedula_usuario': cedula_ingresada,
                'tipo_cedula_usuario': tipo_de_cedula_ingresada
            }
        
    return render_template('enfermero.html')
    
@app.route('/agregar_donacion', methods=['GET', 'POST'])
def agregar_donacion():
    # Obtener datos del usuario de la sesion y el usuario obtenido
    user_data = session.get('user_data')
    user_obtained_data = session.get('enfermero_usuario_obtenido')
    
    # Verificar si el usuario ha iniciado sesión
    if not user_data and user_data.get('enfermero'):
        return render_template('home.html')

    session['enfermero_usuario_verificacion'] = None

    if request.method == 'POST':
        cantidad_sangre_donada = int(request.form.get('cantidad_donada'))
        fecha_donacion = request.form.get('fecha_donacion')
        numero_documento = user_obtained_data['cedula_usuario']
        tipo_documento = user_obtained_data['tipo_cedula_usuario']

        donacion_exitosa = insertarDonacion(numero_documento, tipo_documento, fecha_donacion, cantidad_sangre_donada)
        session['donacion_exitosa'] = donacion_exitosa

    return render_template('agregar_donacion.html')

# Ruta de login y registro.

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verificar si ya hay datos de usuario en la sesión
    if 'user_data' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Obtener datos del formulario
        numero_documento = request.form.get('numero_documento')
        tipo_documento = request.form.get('tipo_documento')
        contrasena = request.form.get('contrasena')

        # Verificar si la cuenta existe y su numero de documento y contraseña son validos.
        exists = verificacionLogin(numero_documento, tipo_documento, contrasena)

        # Almacenar el resultado de la verificación en la sesión
        session['login_verificacion_resultado'] = exists

        if exists:
            usuario = obtenerUsuarioPorDocumento(numero_documento, tipo_documento)

            # Guardar los datos en la sesión
            session['user_data'] = generarUsuarioSesion(usuario.nombre, usuario.contrasena, usuario.correo, usuario.numero_documento, usuario.donante, usuario.admin, 
                                                        usuario.enfermero, usuario.puntos, usuario.total_donado, usuario.tipo_de_sangre, usuario.tipo_documento,
                                                        usuario.perfil_imagen_link, usuario.perfil_imagen_deletehash)

    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # Verificar si ya hay datos de usuario en la sesión
    if 'user_data' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Obtener datos del formulario
        usuario = obtenerValoresRegistro(request)

        # Verificar si la cuenta ya existe
        exists = verificarExistenciaUsuario(usuario.numero_documento, usuario.tipo_documento)

        # Almacenar el resultado de la verificación en la sesión
        session['registarse_verificacion_resultado'] = exists

        # Crear el usuario en el sistema.
        if not exists:
            # Enviar la imagen a Imgur y guardarla.
            imagen = request.files.get('perfil_imagen')
            usuario.perfil_imagen_link, usuario.perfil_imagen_deletehash = generarUsuarioImagen(imagen, imgur_handler)

            registrarUsuario(usuario.nombre, usuario.contrasena, usuario.correo, usuario.numero_documento, usuario.donante, usuario.admin, 
                             usuario.enfermero, usuario.puntos, usuario.total_donado, usuario.tipo_de_sangre, usuario.tipo_documento,
                             usuario.perfil_imagen_link, usuario.perfil_imagen_deletehash)

            # Guardar los datos en la sesión
            session['user_data'] = generarUsuarioSesion(usuario.nombre, usuario.contrasena, usuario.correo, usuario.numero_documento, usuario.donante, usuario.admin, 
                                                        usuario.enfermero, usuario.puntos, usuario.total_donado, usuario.tipo_de_sangre, usuario.tipo_documento,
                                                        usuario.perfil_imagen_link, usuario.perfil_imagen_deletehash)
        
    return render_template('registro.html')


if __name__ == '__main__':
    app.run(debug=True)