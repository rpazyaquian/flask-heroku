__author__ = 'rebecca'

from flask_wtf import Form
from wtforms import TextField, PasswordField, validators


class RegistrationForm(Form):
    username = TextField('Username', validators=[
        validators.Length(min=4, max=80),
        validators.DataRequired()
    ])
    password = PasswordField('Password', validators=[
        validators.Length(min=4, max=16),
        validators.EqualTo('confirm_password', 'Passwords must match.'),
        validators.DataRequired()
    ])
    confirm_password = PasswordField('Repeat Password')


class LoginForm(Form):
    username = TextField('Username', validators=[
        validators.DataRequired()
    ])
    password = PasswordField('Password', validators=[
        validators.DataRequired()
    ])