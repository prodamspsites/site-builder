# coding: utf-8
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField


class LoginForm(Form):
    username = StringField('Usuário', description='Nome de usuário')
    password = PasswordField('Senha', description='Senha do usuário')