# coding: utf-8
from functools import wraps
from flask import redirect, url_for, current_app
from flask_login import current_user

from builder.models import User, Role
from builder.exceptions import RoleNotFound


def login_permission(group):
    """Check if current_user has a permission to see"""
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user = User.query.get(current_user.get_id())
            try:
                permissions = current_app.config['PERMISSION_GROUPS'][group]
                for permission in permissions:
                    role = Role.search_role(name=permission, exactly=True)
                    if user.has_role(role):
                        return function(*args, **kwargs)
            except RoleNotFound:
                return redirect(url_for('security.not_authorized'))
        return wrapper
    return decorator
