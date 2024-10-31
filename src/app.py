#////////////////////////////// Importaciones //////////////////////////////////////////////
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from servicios.flask_imgur_servicio import *

import os
from datetime import datetime

# Controlador para el login y registro
from controladores.aunteticacion_controlador import *

# Controlador para el registro

from controladores.registro_controlador import *

# Base de datos, chatbot.
from servicios.usuario_bd_servicio import *
from servicios.chatbot_servicio import *

# Importar el servicio de sesiones construido.

from servicios.sesion_servicio import *

# app principal del Flask
app = Flask(__name__,
            static_url_path='', 
            static_folder= os.path.join(os.path.pardir, 'static'),
            template_folder= os.path.join(os.path.pardir, 'templates'))

# Imgur client id para la API
app.config["IMGUR_ID"] = secret_config.IMGUR_CLIENT_ID
imgur_handler = Imgur(app)

# Secreto para el App de Flask
app.secret_key = secret_config.SECRET_KEY_FLASK

#////////////////////////////// Rutas //////////////////////////////////////////////

@app.route('/')
def home():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')
    
    # Verificar si el usuario ha iniciado sesión
    if not user_data:
        return render_template('home.html')

    # Verificar si es admin o enfermero y renderizar el template adecuado
    if user_data.get('admin'):
        return render_template('admin.html', user_data=user_data)
    elif user_data.get('enfermero'):
        return render_template('enfermero.html', user_data=user_data)
    else:
        # Se renderiza el home para cada uno.
        return render_template('home.html', user_data=user_data)

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
            session['user_data'] = generar_usuario_sesion(usuario.nombre, usuario.contrasena, usuario.correo, usuario.numero_documento, usuario.donante, usuario.admin, 
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
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        contrasena = request.form.get('contrasena')
        correo = request.form.get('correo')
        numero_documento = request.form.get('numero_documento')
        donante = False
        admin = False
        enfermero = False
        puntos = 0
        total_donado = 0
        tipo_de_sangre = request.form.get('tipo_de_sangre')
        tipo_documento = request.form.get('tipo_documento')
        imagen = request.files.get('perfil_imagen')

        # Definir el nombre completo.
        nombre_completo = nombre + ' ' + apellido

        # Enviar la imagen a Imgur y guardarla.
        perfil_imagen_link, perfil_imagen_deletehash = generar_usuario_imagen(imagen, imgur_handler)

        # Verificar si la cuenta ya existe
        exists = verificarExistenciaUsuario(numero_documento, tipo_documento)

        # Almacenar el resultado de la verificación en la sesión
        session['registarse_verificacion_resultado'] = exists

        # Crear el usuario en el sistema.
        if not exists:
            registrarUsuario(nombre_completo, contrasena, correo, numero_documento, donante, admin, enfermero, puntos, total_donado, tipo_de_sangre, 
                             tipo_documento, perfil_imagen_link, perfil_imagen_deletehash)

            # Guardar los datos en la sesión
            session['user_data'] = generar_usuario_sesion(nombre_completo, contrasena, correo, numero_documento, donante, admin, enfermero, puntos, total_donado,
                                                           tipo_de_sangre, tipo_documento, perfil_imagen_link, perfil_imagen_deletehash)
        
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.clear()  # Eliminar todos los datos de la sesión
    return redirect(url_for('home'))

@app.route('/return_home')
def close_login():
    session['registarse_verificacion_resultado'] = None
    session['login_verificacion_resultado'] = None
    return redirect(url_for('home'))

@app.route('/perfil')
def perfil():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')

    # Verificar si ya hay datos de usuario en la sesión
    if not user_data:
       return redirect(url_for('home'))
    
    # Reiniciar la sesion de registro_creado si existe una vez que este en el perfil
    registro_creado = session['registro_creado']

    if registro_creado:
        session['registro_creado'] = None

    return render_template('perfil.html', user_data=user_data)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get("message")
    response_text = generate_response(user_message)
    return jsonify({"response": response_text})

@app.route('/solicitud_donacion', methods=['GET', 'POST'])
def solicitud_donacion():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')

    # Verificar si ya hay datos de usuario en la sesión
    if not user_data:
       return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Obtener datos del formulario y algunos del usuario
        tipo_registro = 'Solicitud'
        tipo_sangre = user_data['tipo_de_sangre']
        cantidad = request.form.get('cantidad_sangre_donada')
        razon = request.form.get('razon')
        comentarios = request.form.get('comentarios')
        prioridad = request.form.get('prioridad_solicitud')
        fecha = datetime.now().strftime("%Y-%m-%d")
        usuario_documento = user_data['numero_documento']
        usuario_tipo_documento = user_data['tipo_documento']

        # Crear el registro en el sistema.
        registro_creado = crearRegistro(None, tipo_registro, tipo_sangre, cantidad, razon, comentarios, prioridad, fecha, usuario_documento, usuario_tipo_documento)

        # Almacenar el resultado de la operacion
        session['registro_creado'] = registro_creado


    return render_template('solicitud_donacion.html', user_data=user_data)

if __name__ == '__main__':
    app.run(debug=True)
