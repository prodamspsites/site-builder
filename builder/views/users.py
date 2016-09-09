#coding: utf-8
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required

from builder.models import User, UserRole, Role
from builder.forms.user import UserForm, RoleForm
from builder.exceptions import (InvalidUsername, InvalidEmail, InvalidPassword, PasswordMismatch, UserAlreadyExist,
                                RoleAlreadyExist, InvalidRoleName)


blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
@blueprint.route('/list', methods=['GET'])
@login_required
def list_users():
    users = User.query.order_by(User.created_at.asc()).all()
    return render_template('users/list-users.html', users=users)


@login_required
@blueprint.route('/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        try:
            user = User.create(username=form.username.data,
                               email=form.email.data,
                               password=form.password.data,
                               confirm_password=form.password.data)
            flash('Usuário {} criado com sucesso!'.format(user.username), category='success')
            return redirect(url_for('users.list_users'))

        except InvalidUsername:
            flash('Nome de usuário inválido!', category='danger')

        except InvalidEmail:
            flash('Email inválido!', category='danger')

        except InvalidPassword:
            flash('Password inválido!', category='danger')

        except PasswordMismatch:
            flash('Password e confirmação de password não estão iguais!', category='danger')

        except UserAlreadyExist:
            flash('Usuário ou email já existem!', category='danger')

    return render_template('users/add-user.html', form=form)


@login_required
@blueprint.route('/<user_id>', methods=['GET'])
def user_details(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('Usuário não existe!', category='info')
        return redirect(url_for('users.list_users'))
    return render_template('users/details-user.html', user=user)


@login_required
@blueprint.route('/<user_id>/toogle', methods=['GET'])
def toggle_user(user_id):
    user = User.query.get(user_id)
    if user:
        action = 'desativado' if user.active else 'ativado'
        user.toggle_status()
        flash('Usuário {} foi {}.'.format(user.username, action), category='success')

    else:
        flash('Usuário não encontrado!', category='danger')

    return redirect(url_for('users.list_users'))


@login_required
@blueprint.route('/roles', methods=['GET'])
def list_roles():
    roles = Role.query.order_by(Role.id.asc()).all()
    return render_template('users/list-roles.html', roles=roles)


@login_required
@blueprint.route('/add_role', methods=['GET', 'POST'])
def add_role():
    role_form = RoleForm()
    if role_form.validate_on_submit():
        try:
            role = Role.create(name=role_form.name.data,
                               description=role_form.description.data)
            flash('Permissão {} criado com sucesso!'.format(role.name), category='success')
            return redirect(url_for('users.list_roles'))

        except InvalidRoleName:
            flash('Nome da permissão inválida!', category='danger')

        except RoleAlreadyExist:
            flash('Permissão já existe!', category='danger')

    return render_template('users/add-role.html', form=role_form)


@login_required
@blueprint.route('/role/<role_id>/toogle', methods=['GET'])
def toggle_role(role_id):
    role = Role.query.get(role_id)
    if role:
        action = 'desativado' if role.active else 'ativado'
        role.toggle_status()
        flash('Permissão {} foi {}.'.format(role.name, action), category='success')

    else:
        flash('Permissão não encontrada!', category='danger')

    return redirect(url_for('users.list_roles'))


@login_required
@blueprint.route('/<user_id>/role/<role_id>', methods=['GET'])
def set_role(user_id, role_id):
    user = User.query.get(user_id)
    role = Role.query.get(role_id)
    try:
        UserRole.set_role(user, role)
        flash('Permissão {} atrelada ao usuário {} com sucesso'.format(role.name, user.username), category='success')

    except:
        flash('Erro ao adicionar permissão!')

    return redirect(request.referrer)


@login_required
@blueprint.route('/<user_id>/role/<role_id>/remove', methods=['GET'])
def unset_role(user_id, role_id):
    user = User.query.get(user_id)
    role = Role.query.get(role_id)
    try:
        UserRole.delete_role(user, role)
        flash('Permissão {} removida do usuário {} com sucesso'.format(role.name, user.username), category='success')

    except:
        flash('Erro ao remover permissão!')

    return redirect(request.referrer)
