from flask.cli import AppGroup

from App.controllers import *
from App.database import get_migrate
from App.main import create_app

app = create_app()
migrate = get_migrate(app)

init = AppGroup("init")


@init.command("i")
def initialize_database():
    user_azure = create_profile("azure", "password")
    user_cerulean = create_profile("cerulean", "password")

    upload_picture('azure', 'picture_one')
    upload_picture('azure', 'picture_uno')
    upload_picture('azure', 'picture_dos')

    rate_picture(user_cerulean.id, 1, 5)
    rate_picture(user_cerulean.id, 2, 1)

    rate_profile(user_cerulean.id, user_azure.id, 1)
    rate_profile(user_cerulean.id, user_azure.id, 10)

    rate_profile(user_azure.id, user_cerulean.id, 20)

    print("COMPLETED!")

    print(feed.refresh())
    print(feed.refresh())


app.cli.add_command(init)
