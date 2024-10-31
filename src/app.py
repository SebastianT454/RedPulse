#////////////////////////////// Importaciones //////////////////////////////////////////////
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from servicios.flask_imgur_servicio import *
import os

# Controladores para el login y registro
from controladores.aunteticacion_controlador import *

# Base de datos.
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

#////////////////////////////// Funcionalidades //////////////////////////////////////////////
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

@app.route('/logout')
def logout():
    session.clear()  # Eliminar todos los datos de la sesión
    return redirect(url_for('home'))

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
                                                          usuario.enfermero, usuario.tipo_de_sangre, usuario.tipo_documento,  usuario.perfil_imagen_link, usuario.perfil_imagen_deletehash)

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
            registrarUsuario(nombre_completo, contrasena, correo, numero_documento, False, False, False, tipo_de_sangre, tipo_documento, perfil_imagen_link, perfil_imagen_deletehash)

            # Guardar los datos en la sesión
            session['user_data'] = generar_usuario_sesion(nombre_completo, contrasena, correo, numero_documento, False, False, False, tipo_de_sangre, tipo_documento, perfil_imagen_link, perfil_imagen_deletehash)
        
    return render_template('registro.html')

@app.route('/perfil')
def perfil():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')

    # Verificar si ya hay datos de usuario en la sesión
    if not user_data:
       return redirect(url_for('home'))
    
    return render_template('perfil.html', user_data=user_data)

@app.route('/return_home')
def close_login():
    session['registarse_verificacion_resultado'] = None
    session['login_verificacion_resultado'] = None
    return redirect(url_for('home'))

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get("message")
    response_text = generate_response(user_message)
    return jsonify({"response": response_text})


if __name__ == '__main__':
    app.run(debug=True)
