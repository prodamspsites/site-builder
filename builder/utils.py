# coding: utf-8
def register_blueprints(app):
    """Shortcut to register all blueprints of system"""
    from builder.views.security import blueprint as security_blueprint
    from builder.views.dashboard import blueprint as dashboard_blueprint
    from builder.views.users import blueprint as users_blueprint
    from builder.views.core import blueprint as core_blueprint
    app.register_blueprint(security_blueprint)
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(core_blueprint, url_prefix='/core')
    return app


def register_template_filters(app):
    """Shortcut to register all template filters"""
    app.add_template_filter(convert_time, 'strftime')
    return app


def convert_time(date, format=None):
    """Convert to ideal time in templates"""
    if not date:
        return '-'
    if format:
        return date.strftime(format)
    return date.strftime('%d/%m/%Y %H:%M')