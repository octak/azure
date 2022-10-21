from flask.cli import AppGroup

from App import controllers
from App.database import get_migrate
from App.main import create_app

app = create_app()
migrate = get_migrate(app)

init = AppGroup("init")


@init.command("i")
def initialize_database():
    user_azure = controllers.create_profile("azure", "password")
    user_cerulean = controllers.create_profile("cerulean", "password")

    controllers.upload_picture('azure', 'picture_one')
    controllers.upload_picture('azure', 'picture_uno')
    controllers.upload_picture('azure', 'picture_dos')

    controllers.rate_picture(user_cerulean.id, 1, 5)
    controllers.rate_picture(user_cerulean.id, 2, 1)

    controllers.rate_profile(user_cerulean.id, user_azure.id, 1)
    controllers.rate_profile(user_cerulean.id, user_azure.id, 10)

    controllers.rate_profile(user_azure.id, user_cerulean.id, 20)

    print("COMPLETED!")

    print(controllers.refresh())
    print(controllers.refresh())


app.cli.add_command(init)
