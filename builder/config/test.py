# coding: utf-8
from builder.config.base import BaseConfig


class Config(BaseConfig):
    """ Specific config used in test environment """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SECRET_KEY = 'test'

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = 'no-reply@test'
