# coding: utf-8
from flask import Blueprint, render_template
from flask_login import login_required


blueprint = Blueprint('security', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET', 'POST'])
def login():
    return render_template('security/login.html')


@blueprint.route('/support', methods=['GET', 'POST'])
def suppport():
    return render_template('security/support.html')


@blueprint.route('/dashboard', methods=['GET'])
def home():
    return render_template('dashboard/index.html')


@blueprint.route('/config', methods=['GET'])
def config():
    return render_template('dashboard/config.html')


@blueprint.route('/change-password', methods=['GET'])
def change_password():
    return render_template('dashboard/change-password.html')