from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from . import app, db, login_manager
#importar modelo de usuario como Usuario


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contra = request.form['contraseña'] #no se si se llama contraseña en la db
        
        user = Usuario.query.filter_by(email=email).first()
        
        if user and user.confirmar_contra(contra): #confirmar_contra se define en models 
            login_user(Usuario)  # Inicia sesion
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('asa')) #donde se redireccione
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')

    return render_template('login') #se redirecciona al login

@app.route('/logout')
@login_required  
def logout():
    logout_user()  
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('login')) #se redirecciona al login



