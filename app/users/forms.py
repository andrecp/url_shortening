from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired


class SignUpForm(Form):
    username = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class SignInForm(Form):
    username = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
