from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
db = SQLAlchemy()
jwt = JWTManager()


def get_migrate(app):
    return Migrate(app, db)
