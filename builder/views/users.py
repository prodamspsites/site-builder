#coding: utf-8
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from builder.models import User, UserRole, Role
from builder.forms.user import UserForm
from builder.exceptions import (InvalidUsername, InvalidEmail, InvalidPassword, PasswordMismatch, UserAlreadyExist)


blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
@blueprint.route('/list', methods=['GET'])
@login_required
def list_users():
    users = User.query.all()
    return render_template('users/list-users.html', users=users)


@login_required
@blueprint.route('/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        try:
            user = User()
            user = user.create(username=form.username.data,
                               email=form.email.data,
                               password=form.password.data,
                               confirm_password=form.password.data)
            flash('Usuário {} criado com sucesso!'.format(user.username), category='success')
            return redirect(url_for('users.list_users'))

        except InvalidUsername:
            flash('Nome de usuário inválido', category='danger')

        except InvalidEmail:
            flash('Email inválido', category='danger')

        except InvalidPassword:
            flash('Password inválido', category='danger')

        except PasswordMismatch:
            flash('Password e confirmação de password não estão iguais', category='danger')

        except UserAlreadyExist:
            flash('Usuário ou email já existem', category='danger')

    return render_template('users/add-user.html', form=form)


@login_required
@blueprint.route('/<user_id>', methods=['GET'])
def user_details(user_id):
    return render_template('users/user-details.html')


@login_required
@blueprint.route('/<user_id>/delete', methods=['GET'])
def user_delete(user_id):
    return render_template('users/user-details.html')


@login_required
@blueprint.route('/roles', methods=['GET'])
def list_roles():
    return render_template('users/list-roles.html')


@login_required
@blueprint.route('/add_role', methods=['GET'])
def add_role():
    return render_template('users/add-role.html')


@login_required
@blueprint.route('/role/<role_id>', methods=['GET'])
def role_details(role_id):
    return render_template('users/role-details.html')


@login_required
@blueprint.route('/role/<role_id>/delete', methods=['GET'])
def role_delete(role_id):
    return #redirect


@login_required
@blueprint.route('/<user_id>/role/<role_id>', methods=['GET'])
def set_role(user_id, role_id):
    return #redirect

