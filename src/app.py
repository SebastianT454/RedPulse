#////////////////////////////// Importaciones //////////////////////////////////////////////
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

# Controladores para el login y registro
from controladores.aunteticacion_controlador import *

# Base de datos.
from servicios.usuario_bd_servicio import *

# app principal del Flask
app = Flask(__name__, template_folder = os.path.join(os.path.pardir, 'templates'))
app.secret_key = 'j98h3y2qweRTY8uiopASDFGHJKLZXCVBNM,./1234567890-=`~!@#$%^&*()_+[]{}|;:?><'

#////////////////////////////// Funcionalidades //////////////////////////////////////////////
@app.route('/')
def home():
    # Verificar si el usuario ya está registrado
    user_data = session.get('user_data')
    return render_template('home.html', user_data=user_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario
        numero_documento = request.form.get('numero_documento')
        contrasena = request.form.get('contrasena')

        # Verificar si la cuenta existe y su numero de documento y contraseña son validos.
        exists = verificacionLogin(numero_documento, contrasena)

        # Almacenar el resultado de la verificación en la sesión
        session['account_verification_result'] = exists

        if exists:
            usuario = obtenerUsuarioPorDocumento(numero_documento)

            # Guardar los datos en la sesión
            session['user_data'] = {
                'nombre_completo': usuario.nombre,
                'contrasena': usuario.contrasena,
                'correo': usuario.correo,
                'numero_documento': usuario.numero_documento,
                'tipo_documento': usuario.tipo_documento
            }   

    return render_template('login.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/return_home')
def close_login():
    session['account_verification_result'] = None
    return redirect(url_for('home'))

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        contrasena = request.form.get('contrasena')
        correo = request.form.get('correo')
        numero_documento = request.form.get('numero_documento')
        tipo_documento = request.form.get('tipo_documento')

        # Definir el nombre completo.
        nombre_completo = nombre + ' ' + apellido

        # Verificar si la cuenta ya existe
        exists = verificarExistenciaUsuario(numero_documento)

        # Almacenar el resultado de la verificación en la sesión
        session['account_verification_result'] = exists

        # Crear el usuario en el sistema.
        if not exists:
            registrarUsuario(nombre_completo, contrasena, correo, numero_documento, False, False, False, tipo_documento)

            # Guardar los datos en la sesión
            session['user_data'] = {
                'nombre_completo': nombre_completo,
                'contrasena': contrasena,
                'correo': correo,
                'numero_documento': numero_documento,
                'tipo_documento': tipo_documento
            }
        
    return render_template('registrarse.html')


if __name__ == '__main__':
    app.run(debug=True)
