# coding: utf-8
from base64 import b64decode

from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required

from builder.forms import LoginForm, ChangePasswordForm, AcceptForm
from builder.models import User, Invite
from builder.exceptions import UserNotFound, PasswordMismatch, InvalidCredentials, InvalidPassword, InvalidToken


blueprint = Blueprint('security', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET', 'POST'])
def login():
    """Used for login user through web"""
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            user = User.by_email(email)
            user.validate_password(password)
            login_user(user)
            user.reload_stats()
            return redirect(url_for('security.dashboard'))

        except (UserNotFound, InvalidCredentials):
            flash('Email ou senha inválido', category='danger')
            return redirect(url_for('security.login'))

    if current_user.is_authenticated:
        return redirect(url_for('security.dashboard'))

    return render_template('security/login.html', form=form, form_action=url_for('security.login'))


@blueprint.route('/logout', methods=['GET'])
def logout():
    """Logout current user"""
    flash('Usuário deslogado!', category='info')
    logout_user()
    return redirect(url_for('security.login'))


@blueprint.route('/not_authorized', methods=['GET'])
def not_authorized():
    """In case of user access page without permission"""
    return render_template('security/not-authorized.html')


@blueprint.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Default template for welcome"""
    return render_template('security/dashboard.html')


@blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Default view to change password"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        try:
            user.change_password(old_password=form.old_password.data,
                                 password=form.password.data,
                                 confirm_password=form.confirm.data)
            flash('Senha alterada com sucesso!', category='success')
            redirect('dashboard.home')

        except InvalidCredentials:
            flash('Senha do usuário inválida!', category='danger')

        except InvalidPassword:
            flash('A senha tem de ter no mínimo 6 caracteres!', category='danger')

        except PasswordMismatch:
            flash('Os campos senha e confirmação não estão iguais!', category='danger')

    return render_template('security/change-password.html', form=form)


@blueprint.route('/confirm-invite', methods=['GET', 'POST'])
def confirm_invite():
    form = AcceptForm()
    if form.validate_on_submit():
        try:
            invite = Invite.get_invite(form.email.data)
            invite.accept(temporary_token=form.token.data,
                          password=form.password.data,
                          confirm_password=form.confirm.data)
            flash('Usuário ativado com sucesso!', category='success')
            return redirect(url_for('security.login'))

        except InvalidToken:
            flash('O token não é valido!', category='danger')

        except InvalidPassword:
            flash('A senha tem de ter no mínimo 6 caracteres!', category='danger')

        except PasswordMismatch:
            flash('Os campos senha e confirmação não estão iguais!', category='danger')

    else:
        encoded_token = request.args.get('t')

        try:
            email, token = b64decode(encoded_token).decode('utf-8').split(':')
            invite = Invite.get_invite(email)
            invite.view()
            form.email.data = email
            form.token.data = token
            flash('Para validar seu convite, basta cadastrar uma senha.', category='info')

        except:
            flash('Para validar seu convite digite os dados e cadastre uma senha!', category='info')

    return render_template('security/confirm-invite.html', form=form)
