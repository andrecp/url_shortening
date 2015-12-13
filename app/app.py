# -*- coding: utf-8 -*-
import os

import flask
import flask.ext.login as flask_login

from flask_sqlalchemy import SQLAlchemy


# Specify the folder with the templates.
template_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'templates')

# Instantiate the flask app.
app = flask.Flask(__name__, template_folder=template_folder)

# Configure differently if in production.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if os.environ.get('MODE') == 'production':
    app.secret_key = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.secret_key = 'xx'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/production.db'

db = SQLAlchemy(app)

# Configure the app to use flask-login.
login_manager = flask_login.LoginManager()
login_manager.login_view = 'signup_login_view'
login_manager.init_app(app)
