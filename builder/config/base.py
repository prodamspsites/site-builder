#coding: utf-8
import os


class BaseConfig(object):
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