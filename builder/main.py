# coding: utf-8
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()


def register_blueprints(app):
    from builder.views.security import blueprint as security_blueprint
    from builder.views.users import blueprint as users_blueprint
    app.register_blueprint(security_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')
    return app


def create_app():
    """Factory app"""
    config_object = 'builder.config.{}.Config'.format(os.environ.get('AUTH_ENV') or 'local')
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

    lm.user_loader(load_user)
    register_blueprints(app)
    return app