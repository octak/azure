# import os
# from datetime import timedelta

# from flask import Flask
# from flask_cors import CORS
# from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
# from flask_jwt_extended import JWTManager

# # from App.controllers import setup_jwt
# from App.database import create_db
# from App.views import *

# # New views must be imported and added to this list

# views = [index_views, profile_views]


# def add_views(app, views):
#     for view in views:
#         app.register_blueprint(view)


# def loadConfig(app, config):
#     app.config["ENV"] = os.environ.get("ENV", "DEVELOPMENT")
#     if app.config["ENV"] == "DEVELOPMENT":
#         app.config.from_object("App.config")
#     else:
#         app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#             "SQLALCHEMY_DATABASE_URI"
#         )
#         app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
#         app.config["JWT_EXPIRATION_DELTA"] = timedelta(
#             days=int(os.environ.get("JWT_EXPIRATION_DELTA"))
#         )
#         app.config["DEBUG"] = os.environ.get("ENV").upper() != "PRODUCTION"
#         app.config["ENV"] = os.environ.get("ENV")

#     for key, value in config.items():
#         app.config[key] = config[key]


# def create_app(config={}):
#     app = Flask(__name__, static_url_path="/static")    
#     CORS(app)
#     loadConfig(app, config)
#     app.config["JWT_EXPIRATION_DELTA"] = timedelta(days=7)
#     app.config["JWT_SECRET_KEY"] = "aa2bded32cc585d3f37c5319abe8890ad28a697ed66d5823f10536cc9c0fdb9"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config["TEMPLATES_AUTO_RELOAD"] = True
#     app.config["PREFERRED_URL_SCHEME"] = "https"
#     app.config["UPLOADED_PHOTOS_DEST"] = "App/uploads"
#     photos = UploadSet("photos", TEXT + DOCUMENTS + IMAGES)
#     configure_uploads(app, photos)
#     add_views(app, views)
#     create_db(app)
#     # setup_jwt(app)
#     jwt = JWTManager(app)
#     app.app_context().push()
#     return app

import os
from flask import Flask
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta


from App.database import create_db


from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list

views = [
    user_views,
    index_views
]

def add_views(app, views):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'DEVELOPMENT')
    delta = 7
    if app.config['ENV'] == "DEVELOPMENT":
        app.config.from_object('App.config')
        delta = app.config['JWT_EXPIRATION_DELTA']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['DEBUG'] = os.environ.get('ENV').upper() != 'PRODUCTION'
        app.config['ENV'] = os.environ.get('ENV')
        delta = os.environ.get('JWT_EXPIRATION_DELTA', 7)
        
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=int(delta))
        
    for key, value in config.items():
        app.config[key] = config[key]

def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    loadConfig(app, config)
#     app.config['JWT_EXPIRATION_DELTA'] =  timedelta(days=7)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)
    create_db(app)
    # setup_jwt(app)
    app.app_context().push()
    return app

