# coding: utf-8
from flask import Blueprint, render_template
from flask_login import login_required


blueprint = Blueprint('core', __name__, template_folder='templates', static_folder='static')


@blueprint.route('/', methods=['GET'])
@login_required
def list_projects():
    """Default template for welcome"""
    return render_template('core/index.html')