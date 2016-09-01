#coding: utf-8
from flask import Blueprint, render_template
from flask_login import login_required


blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
@blueprint.route('/list', methods=['GET'])
def list_users():
    return render_template('users/list-users.html')


@blueprint.route('/add', methods=['GET'])
def add_user():
    return render_template('users/add-user.html')


@blueprint.route('/<user_id>', methods=['GET'])
def user_details(user_id):
    return render_template('users/user-details.html')


@blueprint.route('/<user_id>/delete', methods=['GET'])
def user_delete(user_id):
    return render_template('users/user-details.html')


@blueprint.route('/roles', methods=['GET'])
def list_roles():
    return render_template('users/list-roles.html')


@blueprint.route('/add_role', methods=['GET'])
def add_role():
    return render_template('users/add-role.html')


@blueprint.route('/role/<role_id>', methods=['GET'])
def role_details(role_id):
    return render_template('users/role-details.html')


@blueprint.route('/role/<role_id>/delete', methods=['GET'])
def role_delete(role_id):
    return #redirect


@blueprint.route('/<user_id>/role/<role_id>', methods=['GET'])
def set_role(user_id, role_id):
    return #redirect

