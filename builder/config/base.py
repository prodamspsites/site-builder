#coding: utf-8
import os
from datetime import datetime


class Config(object):
    """ Basic config shared in all environments """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False

    PERMISSION_GROUPS = {
        'superuser': ['superuser'],
        'admin': ['superuser', 'admin'],
        'client': ['superuser', 'admin', 'client'],
    }

    # Flask Mail Configs
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    INVITE_EXPIRE = 7
