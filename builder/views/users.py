#coding: utf-8
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from builder.models import User, Role, Invite
from builder.forms import RoleForm, InviteForm
from builder.exceptions import (InvalidEmail, UserAlreadyExist, RoleAlreadyExist, InvalidRoleName, EmptyUserName,
                                UserNotHasRole, UserAlreadyInRole)
from builder.views import login_permission


blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
@blueprint.route('/list', methods=['GET'])
@login_required
@login_permission('admin')
def list_users():
    """Return list of all users in database"""
    users = User.query.order_by(User.created_at.asc()).all()
    return render_template('users/list-users.html', users=users)


@blueprint.route('/<user_id>', methods=['GET'])
@login_required
@login_permission('admin')
def user_details(user_id):
    """Get user details and your security groups"""
    user = User.query.get(user_id)
    if not user:
        flash('Usuário não encontrado!', category='danger')
        return redirect(url_for('users.list_users'))
    return render_template('users/details-user.html', user=user)


@blueprint.route('/<user_id>/toggle', methods=['GET'])
@login_required
@login_permission('admin')
def toggle_user(user_id):
    """Toggle status of user"""
    user = User.query.get(user_id)

    if user:
        if user != current_user:
            action = 'desativado' if user.active else 'ativado'
            user.toggle_status()
            flash('Usuário {} foi {}.'.format(user.name, action), category='success')
        else:
            flash('Voce não pode alterar seus próprios usuário!', category='warning')

    else:
        flash('Usuário não encontrado!', category='danger')

    return redirect(url_for('users.list_users'))


@blueprint.route('/roles', methods=['GET'])
@login_required
@login_permission('superuser')
def list_roles():
    """List all roles in database"""
    roles = Role.query.order_by(Role.id.asc()).all()
    return render_template('users/list-roles.html', roles=roles)


@blueprint.route('/add_role', methods=['GET', 'POST'])
@login_required
@login_permission('superuser')
def add_role():
    """Add role in system"""
    form = RoleForm()
    if form.validate_on_submit():
        try:
            role = Role.create(name=form.name.data, description=form.description.data)
            flash('Permissão {} criado com sucesso!'.format(role.name), category='success')
            return redirect(url_for('users.list_roles'))

        except InvalidRoleName:
            flash('Nome da permissão inválida!', category='danger')

        except RoleAlreadyExist:
            flash('Permissão já existe!', category='danger')

    return render_template('users/add-role.html', form=form)


@blueprint.route('/role/<role_id>/toogle', methods=['GET'])
@login_required
@login_permission('superuser')
def toggle_role(role_id):
    """Toggle status of role"""
    role = Role.query.get(role_id)
    if role:
        action = 'desativado' if role.active else 'ativado'
        role.toggle_status()
        flash('Permissão {} foi {}.'.format(role.name, action), category='success')

    else:
        flash('Permissão não encontrada!', category='danger')

    return redirect(url_for('users.list_roles'))


@blueprint.route('/<user_id>/role/<role_id>', methods=['GET'])
@login_required
@login_permission('admin')
def set_role(user_id, role_id):
    """View to set role of user"""
    user = User.query.get(user_id)
    role = Role.query.get(role_id)
    try:
        if role.name == 'superuser' and not current_user.superuser:
            flash('Permissão de superusuário só pode ser atribuída por outro superusuário', category='danger')
        else:
            user.set_role(role)
            flash('Permissão {} atrelada ao usuário {}.'.format(role.name, user.name), category='success')

    except UserAlreadyInRole:
        flash('Usuário já tem essa permissão!', category='info')
    except:
        flash('Erro ao adicionar permissão!', category='danger')

    return redirect(request.referrer)


@blueprint.route('/<user_id>/role/<role_id>/remove', methods=['GET'])
@login_required
@login_permission('admin')
def unset_role(user_id, role_id):
    """View to remove role of user"""
    user = User.query.get(user_id)
    role = Role.query.get(role_id)

    if user == current_user:
        flash('Não pode remover seus próprios acessos!', category='info')
        return redirect(request.referrer)

    try:
        if role.name == 'superuser' and not current_user.superuser:
            flash('Permissão de superusuário só pode ser removida por outro superusuário', category='danger')
        else:
            user.remove_role(role)
            flash('Permissão {} removida do usuário {}.'.format(role.name, user.name), category='success')

    except UserNotHasRole:
        flash('Usuário já não tem essa permissão!', category='info')
    except:
        flash('Erro ao remover permissão!', category='danger')

    return redirect(request.referrer)


@blueprint.route('/invites', methods=['GET', 'POST'])
@login_required
@login_permission('admin')
def invites():
    form = InviteForm()
    if form.validate_on_submit():
        try:
            invite = Invite.create_invite(host=current_user, guest_name=form.name.data, guest_email=form.email.data)
            flash('O usuário {} foi convidado!'.format(invite.guest.name), category='success')

        except UserAlreadyExist:
            flash('O email {} já foi utilizado!'.format(form.email.data), category='warning')

        except EmptyUserName:
            flash('O campo nome está vazio!'.format(form.email.data), category='danger')

        except InvalidEmail:
            flash('O email é inválido!'.format(form.email.data), category='danger')

    invites = Invite.query.all()
    return render_template('users/invites.html', form=form, invites=invites)
