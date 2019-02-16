import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR,  'database')


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '9f032adf045bb72391818a6ded254c75'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'prod.db')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'dev.db')
    DEBUG = True


class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'test.org'
    TESTING = True
