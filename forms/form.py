from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	"""Campos do formuário de login"""
    username = StringField("username", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
