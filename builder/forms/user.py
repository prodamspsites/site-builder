# coding: utf-8
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField


class UserForm(Form):
    username = StringField('Usuário', description='Nome de usuário')
    email = StringField('E-mail', description='Email')
    password = PasswordField('Senha', description='Senha')
    confirm_password = PasswordField('Confirmação de senha', description='Confirmação de senha')
    active = BooleanField('Ativo')
    superuser = BooleanField('Super Usuário')


class RoleForm(Form):
    name = StringField('Nome', description='Nome da permissão')
    description = StringField('Descrição', description='Descrição da permissão')
    active = BooleanField('Ativo')