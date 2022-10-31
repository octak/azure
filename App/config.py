from datetime import timedelta


class Config(object):
    JWT_EXPIRATION_DELTA = timedelta(days=10)
    PREFERRED_URL_SCHEME = 'https'
    SECRET_KEY = "SECRETKEY"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    UPLOADED_PHOTOS_DEST = "App/uploads"


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    TESTING = True
