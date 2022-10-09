import sys

import click
import pytest
from flask import Flask
from flask.cli import AppGroup, with_appcontext

from App.controllers import *
from App.database import create_db, get_migrate
from App.main import create_app
from App.models import *


app = create_app()
migrate = get_migrate(app)
test = AppGroup('test', help='Testing commands.')

@test.command("initialiseDB", help="Attempts to create and set up the database.")
def initialiseDB():
    feed = create_feed()

    user_azure = User(username="azure", password="no-exceptions")
    user_cerulean = User(username="cerulean", password="shayakh-li")
    db.session.add_all([user_azure, user_cerulean])
    db.session.commit()

    profile_azure = new_profile(user_azure)
    profile_cerulean = new_profile(user_cerulean)

    profile_azure.pictures.append(Picture(url="wikipedia.org/azure"))
    profile_cerulean.pictures.append(Picture(url="wikipedia.org/cerulean", profile=profile_cerulean))
    db.session.commit()

    add_picture_to_profile(profile_azure.id, "ru.m.wikipedia.org/izumrud") # Both methods of adding pictures seem to work...

    print("All Pictures:")
    print(get_all_pictures())

    print("Azure's Pictures:")
    print(profile_azure.pictures)

    # rating = ProfileRating(rater=profile_azure, ratee=profile_cerulean, value=3)
    rate_profile(profile_azure.id, profile_cerulean.id, 1)
    rate_profile(profile_azure.id, profile_cerulean.id, 5)

    print(refresh_views())
    print(generate_feed())

    print(refresh_views())
    print(generate_feed())

    print(generate_feed())

    print("Database initialised.")

app.cli.add_command(test)