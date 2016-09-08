# coding: utf-8
def register_blueprints(app):
    from builder.views.security import blueprint as security_blueprint
    from builder.views.dashboard import blueprint as dashboard_blueprint
    from builder.views.users import blueprint as users_blueprint
    app.register_blueprint(security_blueprint)
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    return app


def register_template_filters(app):
    app.add_template_filter(convert_time, 'strftime')
    return app


def convert_time(date, format=None):
    if not date:
        return '-'
    if format:
        return date.strftime(format)
    return date.strftime('%d/%m/%Y %H:%M')