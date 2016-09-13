# coding: utf-8
from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required


blueprint = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
@login_required
def home():
    """Default template for welcome"""
    return render_template('dashboard/index.html')


@blueprint.route('/config', methods=['GET'])
def config():
    """Default template for configuration"""
    return render_template('dashboard/config.html')


@blueprint.route('/change-password', methods=['GET'])
def change_password():
    """Default view to change password"""
    return render_template('dashboard/change-password.html')