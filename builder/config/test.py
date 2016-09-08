# coding: utf-8
from builder.config.base import BaseConfig


class Config(BaseConfig):
    """ Specific config used in test environment """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SECRET_KEY = 'test'