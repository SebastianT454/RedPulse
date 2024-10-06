from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key' #secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'db' #base de datos

db = SQLAlchemy(app) 
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirige a la vista de login si no está autenticado

# Importa tus rutas
from . import rutas
