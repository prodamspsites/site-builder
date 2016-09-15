# coding: utf-8
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField


class LoginForm(Form):
    """Form used for login user"""
    username = StringField('Usuário', description='Nome de usuário')
    password = PasswordField('Senha', description='Senha do usuário')


class UserForm(Form):
    """Form to create and edit user"""
    username = StringField('Usuário', description='Nome de usuário')
    email = StringField('E-mail', description='Email')
    name = StringField('Nome completo', description='Nome Completo')
    password = PasswordField('Senha', description='Senha')
    confirm_password = PasswordField('Confirmação de senha', description='Confirmação de senha')
    active = BooleanField('Ativo')
    superuser = BooleanField('Super Usuário')


class RoleForm(Form):
    """Form to create and edit role"""
    name = StringField('Nome', description='Nome da permissão')
    description = StringField('Descrição', description='Descrição da permissão')
    active = BooleanField('Ativo')


class ChangePasswordForm(Form):
    old_password = PasswordField('Senha Antiga', description='Senha Antiga')
    password = PasswordField('Senha', description='Nova senha')
    confirm = PasswordField('Confirmação', description='Confirmação de senha')