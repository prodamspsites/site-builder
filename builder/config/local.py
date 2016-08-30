# coding: utf-8
from builder.config.base import BaseConfig


class Config(BaseConfig):
    """ Specific config used in local environment """
    DEBUG = True
    SECRET_KEY = 'itsasecret'
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:auth@localhost:5432/flapy_auth'
