import sys

import click
import pytest
from flask import Flask
from flask.cli import AppGroup, with_appcontext

from App.controllers import *
from App.database import create_db, get_migrate
from App.main import create_app


app = create_app()
migrate = get_migrate(app)
test = AppGroup("test", help="Testing commands.")


@test.command("i", help="Attempts to create and set up the database.")
def initialiseDB():
    feed = create_feed()

    user_azure = create_profile("azure", "no-exceptions")
    user_azure2 = create_profile("azure", "no-exceptions")
    user_cerulean = create_profile("cerulean", "shayach-li")

    upload_picture("azure", "wikipedia.org/azure")
    upload_picture(user_cerulean.id, "wikipedia.org/cerulean")

    print("All Pictures:", end="")
    print(Picture.query.all())

    print("Azure's Pictures:", end="")
    print(get_uploaded_pictures("azure"))

    rate_profile(user_azure.id, user_cerulean.id, 1)
    rate_profile(user_azure.id, user_cerulean.id, 5)

    print("Database initialised.")

app.cli.add_command(test)
