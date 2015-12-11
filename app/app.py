import flask
import flask.ext.login as flask_login

app = flask.Flask(__name__)
app.secret_key = 'xx'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
