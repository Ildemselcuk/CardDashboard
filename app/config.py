# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os


class Config(object):
    # for Product model
    CURRENCY = {'usd': 'usd', 'eur': 'eur'}
    STATE = {'completed': 1, 'pending': 2, 'refunded': 3}
    PAYMENT_TYPE = {'cc': 1, 'paypal': 2, 'wire': 3}

    USERS_ROLES = {'ADMIN': 1, 'USER': 2}
    USERS_STATUS = {'ACTIVE': 1, 'SUSPENDED': 2}

    # USERS_STATUS = { 'ACTIVE' :1 , 'SUSPENDED' : 2 }
    # check verified_email
    VERIFIED_EMAIL = {'verified': 1, 'not-verified': 2}

    LOGIN_ATTEMPT_LIMIT = 10

    DEFAULT_IMAGE_URL = 'static/assets/images/'

   

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    # SECRET_KEY = config('SECRET_KEY'  , default='S#perS3crEt_007')
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_007')
    SECURITY_PASSWORD_SALT = "146585145368132386173505678016728509634"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_IMAGES_DEST = 'uploads/images'
    UPLOADED_PATH = os.path.join(basedir, 'uploads'),
    JSON_SORT_KEYS = False


    # This will create a file in <app> FOLDER
    # Database init
    mysql_password = os.environ.get('MYSQL_PASSWORD') or 'db1db1'
    mysql_user = os.environ.get('MYSQL_USER') or 'db1'
    mysql_database = os.environ.get('MYSQL_DATABASE') or 'db1'
    mysql_host = os.environ.get('MYSQL_HOST') or 'db'
    mysql_port = os.environ.get('MYSQL_PORT') or '3307'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{mysql_user}:{mysql_password}@' \
                              f'{mysql_host}:{mysql_port}/{mysql_database}'
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600
    }
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    WTF_CSRF_ENABLED = False

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE', 'mysql+pymysql'),
        os.getenv('DB_USERNAME', os.environ.get('MYSQL_USER') or 'db1'),
        os.getenv('DB_PASS', os.environ.get('MYSQL_PASSWORD') or 'db1db1'),
        os.getenv('DB_HOST', os.environ.get('MYSQL_HOST') or 'db'),
        os.getenv('DB_PORT', os.environ.get('MYSQL_PORT') or 3307),
        os.getenv('DB_NAME', os.environ.get('MYSQL_DATABASE') or 'db1')
    )


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
