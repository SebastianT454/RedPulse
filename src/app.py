#////////////////////////////// Importaciones //////////////////////////////////////////////
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

#Imgur
from servicios.Misc.flask_imgur_servicio import *

#Misc
import os

# Controlador para el login y registro
from controladores.aunteticacion_controlador import *

# Controlador de puntos
from controladores.puntos_controlador import *

# Controlador de solicitudes pendientes
from controladores.solicitudes_pendientes_controlador import *

# Base de datos
from servicios.BaseDeDatos.usuario_bd_servicio import *
from servicios.BaseDeDatos.registro_bd_servicio import *

# Chabot
from servicios.chatbot_servicio import *

# Importar el servicio de sesiones construido.
from servicios.sesion_servicio import *

# Importar el servicio de donaciones.
from servicios.registro_servicio import *

#email
from servicios.notificaciones_servicio import *
email = Notificaciones()

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

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/informacion_preparativos')
def informacion_preparativos():
    return render_template('informacion_preparativos.html')

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

@app.route('/movimientos', methods=['GET', 'POST'])
def movimientos():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')

    # Verificar si ya hay datos de usuario en la sesión
    if not user_data:
       return redirect(url_for('home'))

    return render_template('movimientos.html', user_data=user_data)

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
    if request.method == 'POST':
        data = request.get_json()
        usuario_mensaje_ingresado = data.get("mensaje_ingresado")
        respuesta = generate_response(usuario_mensaje_ingresado)
        return jsonify(respuesta=respuesta)
    
    return render_template('chatbot.html')

@app.route('/solicitud_donacion', methods=['GET', 'POST'])
def solicitud_donacion():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')

    # Verificar si ya hay datos de usuario en la sesión
    if not user_data:
       return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Crear el registro en el sistema.
        registro_creado = crearRegistro(request, user_data)

        # Almacenar el resultado de la operacion
        session['registro_creado'] = registro_creado

    return render_template('solicitud_donacion.html', user_data=user_data)

# Rutas de administrador (estadisticas y solicitudes pendientes)

@app.route('/solicitudes_pendientes', methods=['GET', 'POST'])
def solicitudes_pendientes():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')
    
    # Verificar si el usuario ha iniciado sesión, es admin y no es enfermero
    if not user_data or not user_data.get('admin'):
        return redirect(url_for('home'))
    
    # Obtener las solicitudes pendientes
    solicitudes = obtenerSolicitudesPendientes()
    
    if request.method == 'POST':
        data = request.get_json()
        solicitud_id = data.get('id')
        accion = data.get('accion')
        tipo_sangre_solicitud = data.get('tipo_sangre')

        actualizarEstadoRegistro(solicitud_id, accion)
        verificarNivelesDeSangre(solicitud_id, accion, tipo_sangre_solicitud)

    return render_template('solicitudes_pendientes.html', solicitudes_pendientes=json.dumps(solicitudes))

@app.route('/estadisticas')
def estadisticas():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')
    
    # Verificar si el usuario ha iniciado sesión
    if not user_data or not user_data.get('admin'):
        return redirect(url_for('home'))
    
    # Obtener datos de las estadisticas
    donaciones_por_mes = obtenerDonacionesPorMes()
    sangre_por_tipo = obtenerCantidadDeSangrePorTipo()

    return render_template('estadisticas.html', 
                           donaciones_por_mes=json.dumps(donaciones_por_mes), 
                           sangre_por_tipo=json.dumps(sangre_por_tipo) )

# Rutas para el enfermero

@app.route('/enfermero', methods=['GET', 'POST'])
def enfermero():
    # Obtener datos del usuario desde la sesión
    user_data = session.get('user_data')
    
    # Verificar si el usuario ha iniciado sesión
    if not user_data or not user_data.get('enfermero'):
        if user_data.get('admin'):
            return redirect(url_for('home'))

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
        
    return render_template('enfermero.html', nombre_enfermero = user_data['nombre'])
    
@app.route('/agregar_donacion', methods=['GET', 'POST'])
def agregar_donacion():
    # Obtener datos del usuario de la sesion y el usuario obtenido
    user_data = session.get('user_data')
    user_obtained_data = session.get('enfermero_usuario_obtenido')
    
    # Verificar si el usuario ha iniciado sesión
    if not user_data or not user_data.get('enfermero'):
        return redirect(url_for('home'))

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
    
    if 'cambio_contrasena_exitoso' in session:
        session['cambio_contrasena_exitoso'] = None

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
            session['user_data'] = generarUsuarioSesion(usuario.nombre, usuario.contrasena, None, usuario.correo, usuario.numero_documento, usuario.donante, usuario.admin, 
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
        usuario = obtenerValoresUsuario(request)

        # Verificar si la cuenta ya existe
        exists = verificarExistenciaUsuario(usuario.numero_documento, usuario.tipo_documento)
        correo_existe = verificarCorreo(usuario.correo)

        # Almacenar el resultado de la verificación en la sesión
        session['registarse_verificacion_resultado'] = True

        # Crear el usuario en el sistema.
        if not exists and not correo_existe:
            # Almacenar el resultado de la verificación en la sesión
            session['registarse_verificacion_resultado'] = False

            # Enviar la imagen a Imgur y guardarla.
            imagen = request.files.get('perfil_imagen')


            usuario.perfil_imagen_link, usuario.perfil_imagen_deletehash = generarUsuarioImagen(imagen, imgur_handler)

            # Crear codigo de recuperacion
            usuario.codigo_recuperacion = secrets.token_urlsafe(16)

            registrarUsuario(usuario.nombre, usuario.contrasena, usuario.codigo_recuperacion, usuario.correo, usuario.numero_documento, usuario.donante, usuario.admin, 
                             usuario.enfermero, usuario.puntos, usuario.total_donado, usuario.tipo_de_sangre, usuario.tipo_documento,
                             usuario.perfil_imagen_link, usuario.perfil_imagen_deletehash)

            # Guardar los datos en la sesión
            session['user_data'] = generarUsuarioSesion(usuario.nombre, usuario.contrasena, None, usuario.correo, usuario.numero_documento, usuario.donante, 
                                                        usuario.admin, usuario.enfermero, usuario.puntos, usuario.total_donado, usuario.tipo_de_sangre, usuario.tipo_documento,
                                                        usuario.perfil_imagen_link, usuario.perfil_imagen_deletehash)
        
    return render_template('registro.html')

# Apartados de solicitar y reestablecer contraseña

@app.route('/solicitar_recuperacion', methods=['GET', 'POST'])
def solicitar_recuperacion():
    # Verificar si ya hay datos de usuario en la sesión
    if 'user_data' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        obtained_email = request.form.get('correo')

        # Verificar si el correo está registrado
        if not verificarCorreo(obtained_email):
            session['correo_valido_resultado'] = False
            return render_template('solicitar_recuperacion.html')

        # Correo valido
        session['correo_valido_resultado'] = True

        codigo = obtenerCodigoRecuperacion(obtained_email)

        # Guardar codigo de recuperacion
        session['correo_recuperacion'] = codigo
        session['correo_recuperacion_asociado'] = obtained_email

        # Enviar notificación por correo con el enlace de recuperación
        email.recuperar_contra_notificacion(obtained_email, codigo)
    
    return render_template('solicitar_recuperacion.html')

@app.route('/reestablecer_contrasena', methods=['GET', 'POST'])
def reestablecer_contrasena():
    # Verificar si ya hay datos de usuario en la sesión
    if 'user_data' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        codigo_recuperacion = session['correo_recuperacion']
        codigo_recuperacion_ingresado = request.form.get('codigo_recuperacion')

        nueva_contrasena = request.form.get('nueva_contrasena')
        confirmacion_nueva_contrasena = request.form.get('confirmacion_nueva_contrasena')

        # verificar si el codigo ingresado y las contraseñas son iguales.
        if codigo_recuperacion != codigo_recuperacion_ingresado or nueva_contrasena != confirmacion_nueva_contrasena:
            session['cambio_contrasena_exitoso'] = False
            return render_template('reestablecer_contrasena.html')
        
        session['cambio_contrasena_exitoso'] = True

        actualizarContrasena(session['correo_recuperacion_asociado'], nueva_contrasena)
        session['correo_recuperacion'] = None
        session['correo_recuperacion_asociado'] = None
        session['correo_valido_resultado'] = None
    
    return render_template('reestablecer_contrasena.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000) # debug=True --> cuando se use localmente
