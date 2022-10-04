import sys

import click
import pytest
from flask import Flask
from flask.cli import AppGroup, with_appcontext

# from App.controllers import ( create_user, get_all_users_json, get_all_users, upload_image)
from App.controllers import *
from App.models import *
from App.database import create_db, get_migrate
from App.main import create_app

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print('database intialized')


'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands')

# Then define the command and any parameters and annotate it with the group (@)


@user_cli.command("create", help="Creates a user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    if create_user(username, password):
        print(f'Created user `{username}`.')
    else:
        print(f'Could not create user. User `{username}` already exists.')

# this command will be : flask user create bob bobpass


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli)  # add the group to the cli


@user_cli.command("upload", help="Uploads a profile picture")
@click.argument("username")
@click.argument("url")
def upload_command(username, url):
    user = get_user_by_username(username)
    if not user:
        print(f'User `{username}` does not exist.')
        return
    upload_image(user.id, url)

@user_cli.command("displayUserPics", help="Displays all a users profile pictures")
@click.argument("username")
def displayUserPics_command(username):
    user = get_user_by_username(username)
    if not user:
        print(f'User `{username}` does not exist.')
        return
    print(get_all_pictures_json())

@user_cli.command("test", help="Displays all a users profile pictures")
def test_command():
    testy = Feed()
    db.session.add(testy)
    db.session.commit()

'''
Generic Commands
'''


@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)
