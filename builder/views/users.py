#coding: utf-8
from flask import Blueprint, render_template
from flask_login import login_required

from builder.models import User, UserRole, Role


blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
@blueprint.route('/list', methods=['GET'])
@login_required
def list_users():
    users = User.query.all()
    return render_template('users/list-users.html', users=users)


@login_required
@blueprint.route('/add', methods=['GET'])
def add_user():
    return render_template('users/add-user.html')


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

