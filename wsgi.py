# from flask.cli import AppGroup

# from App import controllers as cts
from App.extensions import get_migrate
from App.main import create_app

app = create_app()
migrate = get_migrate(app)

# init = AppGroup("init")

# @init.command("i")
# def initialize_database():
#     u1 = cts.create_profile('u1', 'p1')
#     u2 = cts.create_profile('u2', 'p2')
#     u3 = cts.create_profile('u3', 'p2')
#
#     cts.create_picture(u1.id, '猫')
#     cts.create_picture(u1.id, '图')
#     cts.create_picture(u1.id, '片')
#
#     cts.rate_picture(u1.id, 1, 10)
#     cts.rate_picture(u1.id, 2, 5)
#     cts.rate_picture(u1.id, 3, 10)
#
#     cts.rate_profile(u1.id, u2.id, 10)
#     cts.rate_profile(u1.id, u2.id, 20)
#
#     cts.rate_profile(u2.id, u1.id, 50)
#     cts.rate_profile(u3.id, u1.id, 26)
#
#     print('Setup Complete !')
#     print(f'Average Rating of UUID1 : {cts.get_average_rating_for_profile(u1.id)}')
#     print('')
#
#     print('Users :')
#     print(cts.get_profiles())
#     print(f'User1 {cts.get_profiles()[0].username}')
#     print('')
#
#     print('User 1"s Posts :')
#     print(u1.pictures)
#
#     print(cts.to_dict_profiles([u1, u2, u3]))
#
#
# app.cli.add_command(init)
