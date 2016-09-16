# coding: utf-8
from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required

from builder.forms import LoginForm, ChangePasswordForm
from builder.models import User
from builder.exceptions import UserNotFound, PasswordMismatch, InvalidCredentials, InvalidPassword


blueprint = Blueprint('security', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET', 'POST'])
def login():
    """Used for login user through web"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = User.by_login(username)
            if user.validate_password(password):
                login_user(user)
                user.reload_stats()
                return redirect(url_for('dashboard.home'))
            else:
                raise PasswordMismatch

        except (UserNotFound, PasswordMismatch):
            flash('Usuário ou senha inválido', category='danger')
            return redirect(url_for('security.login'))

        except:
            flash('Ocorreu um erro inesperado, tente mais tarde', category='info')
            return redirect(url_for('security.login'))

    if current_user.is_authenticated:
        return redirect(url_for('security.dashboard'))

    return render_template('security/login.html', form=form, form_action=url_for('security.login'))


@blueprint.route('/support', methods=['GET', 'POST'])
def suppport():
    """Return page of support"""
    return render_template('security/support.html')


@blueprint.route('/logout', methods=['GET'])
def logout():
    """Logout current user"""
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

        except:
            flash('Não foi possível alterar a senha, tente mais tarde!', category='info')

    return render_template('security/change-password.html', form=form)
