# coding: utf-8
from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required, current_user

from builder.forms import ChangePasswordForm
from builder.models import User
from builder.exceptions import InvalidCredentials, InvalidPassword, PasswordMismatch


blueprint = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
@login_required
def home():
    """Default template for welcome"""
    return render_template('dashboard/index.html')


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

    return render_template('dashboard/change-password.html', form=form)