import pytest

from App.config import DevelopmentConfig
from App.controllers import *
from App.main import create_app


def delete_all_rows():
    db.session.query(Profile).delete()
    db.session.query(Picture).delete()
    db.session.query(ProfileRating).delete()
    db.session.query(PictureRating).delete()
    db.session.commit()


@pytest.fixture(autouse=True, scope="session")
def app():
    app = create_app(config=DevelopmentConfig)

    yield app.test_client()

    db.drop_all()


@pytest.fixture(scope="function")
def new_user():
    user = create_profile('username', 'password')

    yield user

    delete_all_rows()


@pytest.fixture(scope="function")
def new_users():
    user1 = create_profile('username1', 'password')
    user2 = create_profile('username2', 'password')
    user3 = create_profile('username3', 'password')

    yield [user1, user2, user3]

    delete_all_rows()


@pytest.fixture(scope="function")
def new_picture():
    user = create_profile('username', 'password')
    picture = create_picture(user.id, "url")

    yield picture

    delete_all_rows()


@pytest.fixture(scope="function")
def new_pictures():
    user = create_profile('username', 'password')
    picture1 = create_picture(user.id, "url1")
    picture2 = create_picture(user.id, "url2")
    picture3 = create_picture(user.id, "url3")

    yield [picture1, picture2, picture3]

    delete_all_rows()


@pytest.fixture(scope="function")
def new_picture_with_user():
    user = create_profile('username', 'password')
    picture = create_picture(user.id, "url")

    yield user, picture

    delete_all_rows()
