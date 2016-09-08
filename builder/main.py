# coding: utf-8
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from builder.utils import register_blueprints, register_template_filters


db = SQLAlchemy()


def create_app():
    """Factory app"""
    config_object = 'builder.config.{}.Config'.format(os.environ.get('BUILDER_ENV') or 'local')
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.debug = app.config['DEBUG']

    db.init_app(app)

    lm = LoginManager()
    lm.init_app(app)

    def load_user(user_id):
        try:
            from builder.models import User
            return User.query.get(user_id)
        except ValueError:
            pass

    # Flask login settings
    lm.user_loader(load_user)
    lm.login_view = "security.login"
    lm.needs_refresh_message = "Sessão expirada"
    lm.needs_refresh_message_category = "info"
    lm.login_message = "Faça o login antes de continuar"
    lm.login_message_category = "info"

    register_blueprints(app)
    register_template_filters(app)

    return app