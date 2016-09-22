# coding: utf-8
from flask_mail import Message


def register_blueprints(app):
    """Shortcut to register all blueprints of system"""
    from builder.views.security import blueprint as security_blueprint
    from builder.views.users import blueprint as users_blueprint
    from builder.views.core import blueprint as core_blueprint
    app.register_blueprint(security_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(core_blueprint, url_prefix='/core')
    return app


def register_template_filters(app):
    """Shortcut to register all template filters"""
    app.add_template_filter(convert_time, 'strftime')
    return app


def convert_time(date, format='%d/%m/%Y %H:%M'):
    """
    Convert to ideal time in templates
    :param date: Date time object
    :param format: Format of return
    :return: Format date like format param
    """
    try:
        string = date.strftime(format)
        return string
    except:
        return '-'


def send_email(sender, recipient, subject, html, cc=None, bcc=None):
    """
    This function sent email to valid email using flask-mail
    :param sender: Sender of email, like no-reply@something.com
    :param recipient: Destination of this email
    :param subject: Subject, in string
    :param html: Body html in string, can use render_template
    :param cc: Carbon Copy of this email
    :param bcc: Blind Carbon Copy of this email
    :return: None, just sent email in assyncronous task.
    """
    from builder.main import mail
    message = Message(subject=subject, sender=sender, recipients=[recipient], cc=cc, bcc=bcc, html=html)
    mail.send(message)
