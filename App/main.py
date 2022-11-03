from flask import Flask

from App.config import ProductionConfig
from App.extensions import db, jwt
from App.views import index_views, profile_views

views = [index_views, profile_views]

extensions = [db, jwt]


def create_app(config=ProductionConfig):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config)
    app.app_context().push()

    for view in views:
        app.register_blueprint(view)

    for extension in extensions:
        extension.init_app(app)

    db.drop_all()
    db.create_all()

    return app
