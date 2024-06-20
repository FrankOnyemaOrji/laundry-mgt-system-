import os
from decouple import config
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# uri = config('DATABASE_URL')
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)


class Config:
    SECRET_KEY = config('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=50)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG = config('DEBUG', default=False, cast=bool)


# class ProdConfig(Config):
#     SQLALCHEMY_DATABASE_URI = uri
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ECHO = False
#     DEBUG = config('DEBUG', default=False, cast=bool)


config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    # 'prod': ProdConfig
}
