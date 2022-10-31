from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from App.config import ProductionConfig
from App.database import db
from App.views import index_views, profile_views

views = [
    index_views,
    profile_views
]


def create_app(config=ProductionConfig):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config)
    app.app_context().push()

    CORS(app)
    JWTManager(app)

    for view in views:
        app.register_blueprint(view)

    db.init_app(app)
    db.create_all()

    return app
