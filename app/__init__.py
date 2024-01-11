import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab23hjlOp9'
if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(__file__), 'database'))):
    os.makedirs(os.path.normpath(os.path.join(os.path.dirname(__file__), 'database')))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.normpath(os.path.join(os.path.dirname(__file__), 'database/app.db'))
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import models
from app import database
from app import views
from app import forms
from app import requests