# coding: utf-8
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField


class LoginForm(Form):
    """Form used for login user"""
    email = StringField('Email', description='Email de usuário')
    password = PasswordField('Senha', description='Senha do usuário')


class UserForm(Form):
    """Form to create and edit user"""
    email = StringField('E-mail', description='Email')
    name = StringField('Nome completo', description='Nome Completo')
    password = PasswordField('Senha', description='Senha')
    confirm_password = PasswordField('Confirmação de senha', description='Confirmação de senha')
    active = BooleanField('Ativo')
    superuser = BooleanField('Super Usuário')


class InviteForm(Form):
    """Form to invite new user"""
    email = StringField('E-mail', description='Email')
    name = StringField('Nome completo', description='Nome Completo')


class AcceptForm(Form):
    """Form to accept invite"""
    email = StringField('Email', description='Email')
    token = StringField('Token', description='Token')
    password = PasswordField('Senha', description='Nova senha')
    confirm = PasswordField('Confirmação', description='Confirmação de senha')


class RoleForm(Form):
    """Form to create and edit role"""
    name = StringField('Nome', description='Nome da permissão')
    description = StringField('Descrição', description='Descrição da permissão')
    active = BooleanField('Ativo')


class ChangePasswordForm(Form):
    """Form to change password"""
    old_password = PasswordField('Senha Antiga', description='Senha Antiga')
    password = PasswordField('Senha', description='Nova senha')
    confirm = PasswordField('Confirmação', description='Confirmação de senha')
