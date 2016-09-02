# coding: utf-8
from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required, login_user, logout_user

from builder.forms import security
from builder.models import User
from builder.exceptions import UserNotFound, PasswordMismatch


blueprint = Blueprint('security', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET', 'POST'])
def login():
    login_form = security.LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        try:
            user = User.by_login(username)
            if user.validate_password(password):
                login_user(user)
                return redirect(url_for('security.home'))
            else:
                raise PasswordMismatch

        except (UserNotFound, PasswordMismatch):
            flash('Usuário ou senha inválido', category='danger')
            return redirect(url_for('security.login'))

        except:
            flash('Ocorreu um erro inesperado, tente mais tarde', category='info')
            return redirect(url_for('security.login'))

    return render_template('security/login.html', login_form=login_form, form_action=url_for('security.login'))


@blueprint.route('/support', methods=['GET', 'POST'])
def suppport():
    return render_template('security/support.html')


@blueprint.route('/not_authorized', methods=['GET'])
def not_authorized():
    return render_template('dashboard/not-authorized.html')


@blueprint.route('/dashboard', methods=['GET'])
@login_required
def home():
    return render_template('dashboard/index.html')


@blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('security.login'))


@blueprint.route('/config', methods=['GET'])
def config():
    return render_template('dashboard/config.html')


@blueprint.route('/change-password', methods=['GET'])
def change_password():
    return render_template('dashboard/change-password.html')