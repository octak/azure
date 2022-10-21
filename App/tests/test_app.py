import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import Profile, Picture, PictureRating
from App.controllers import *

from wsgi import app

from App.controllers import profile as profile_controller
from App.controllers import feed as feed_controller

LOGGER = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)

    yield app.test_client()


def test_create_new_profile(empty_db):
    test_profile = create_profile('test_create_new_profile', 'password')
    assert test_profile.username == 'test_create_new_profile'
    assert test_profile.password != 'password'
    assert test_profile.tier == 1
    assert test_profile.tier_points == 0
    assert test_profile.times_rated == 0
    assert test_profile.total_rating == 0
    assert test_profile.average_rating == 0
    assert test_profile.remaining_views == 2
    assert test_profile.pictures == []
    assert test_profile.profile_ratings == []
    assert test_profile.picture_ratings == []


def test_create_duplicate_profile(empty_db):
    test_profile = create_profile('test_create_duplicate_profile', 'password')
    test_profile2 = create_profile('test_create_duplicate_profile', 'password')
    assert test_profile2 is None


def test_check_correct_password(empty_db):
    test_profile = create_profile('test_check_correct_password', 'password')
    assert test_profile.check_password('password') is True


def test_check_incorrect_password(empty_db):
    test_profile = create_profile('test_check_incorrect_password', 'password')
    assert test_profile.check_password('sisma') is False


def test_serialize(empty_db):
    test_profile = create_profile('test_serialize', 'password')
    expected_dict = {
        'id': test_profile.id,
        'username': 'test_serialize',
        'tier': 1,
        'average_rating': 0,
        'pictures': {}
    }
    assert test_profile.serialize() == expected_dict


def test_update_profile_rating(empty_db):
    test_profile = create_profile('test_update_profile_rating', 'password')

    test_profile.update_rating(4, True)
    assert test_profile.times_rated == 1
    assert test_profile.total_rating == 4
    assert test_profile.average_rating == 4

    test_profile.update_rating(2, True)
    assert test_profile.times_rated == 2
    assert test_profile.total_rating == 6
    assert test_profile.average_rating == 3

    test_profile.update_rating(2, False)
    assert test_profile.times_rated == 2
    assert test_profile.total_rating == 8
    assert test_profile.average_rating == 4


def test_create_picture(empty_db):
    test_profile = create_profile('test_create_picture', 'password')
    test_picture = Picture(url='test_create_picture', profile=test_profile)
    db.session.add(test_picture)
    db.session.commit()

    assert test_picture.id == 1
    assert test_picture.profile_id == test_profile.id
    assert test_picture.times_rated == 0
    assert test_picture.total_rating == 0
    assert test_picture.average_rating == 0


def test_serialize_picture(empty_db):
    test_profile = create_profile('test_serialize_picture', 'password')
    test_picture = Picture(url='test_serialize_picture', profile=test_profile)
    db.session.add(test_picture)
    db.session.commit()

    expected_dict = {
        'id': test_picture.id,
        'url': 'test_serialize_picture',
        'average_rating': 0
    }

    assert test_picture.serialize() == expected_dict


def test_update_picture_rating(empty_db):
    test_profile = create_profile('test_update_picture_rating', 'password')
    test_picture = Picture(url='test_update_picture_rating', profile=test_profile)
    db.session.add(test_picture)
    db.session.commit()

    test_picture.update_rating(4, True)
    assert test_picture.times_rated == 1
    assert test_picture.total_rating == 4
    assert test_picture.average_rating == 4

    test_picture.update_rating(2, True)
    assert test_picture.times_rated == 2
    assert test_picture.total_rating == 6
    assert test_picture.average_rating == 3

    test_picture.update_rating(2, False)
    assert test_picture.times_rated == 2
    assert test_picture.total_rating == 8
    assert test_picture.average_rating == 4


def test_get_uploader(empty_db):
    test_profile = create_profile('test_get_uploader', 'password')
    test_picture = Picture(url='test_get_uploader', profile=test_profile)
    db.session.add(test_picture)
    db.session.commit()

    assert test_picture.profile == test_profile


def test_feed_refresh():
    assert feed_controller.refresh('App/test_feed_refresh.json') is True
    assert feed_controller.refresh('App/test_feed_refresh.json') is False


def test_create_picture_rating():
    test_rating = PictureRating(rater_id=1, ratee_id=2, value=5)
    assert test_rating.rater_id == 1
    assert test_rating.ratee_id == 2
    assert test_rating.value == 5


def test_create_profile_rating():
    test_rating = ProfileRating(rater_id=1, ratee_id=2, value=5)
    assert test_rating.rater_id == 1
    assert test_rating.ratee_id == 2
    assert test_rating.value == 5


def test_update_username(empty_db):
    test_profile = create_profile('test_update_username', 'password')
    create_profile('cannot_rename', 'password')

    assert profile_controller.update_username(test_profile.username, 'test_updated_username') is True
    assert profile_controller.update_username(test_profile.username, 'cannot_rename') is False
    assert test_profile.username == 'test_updated_username'


def test_generate_feed(empty_db):
    pass  # not sure about this one


def test_refresh_views(empty_db):
    profiles == profile_controller.get_all_profiles()
    feed_controller.refresh()


def test_rate_profile(empty_db):
    test_profile1 = create_profile('test_rate_profile', 'password')
    test_profile2 = create_profile('test_rate_profile2', 'password')
    test_profile3 = create_profile('test_rate_profile3', 'password')

    profile_controller.rate_profile(test_profile1.id, test_profile2.id, 5)
    assert test_profile2.times_rated == 1
    assert test_profile2.total_rating == 5
    assert test_profile2.average_rating == 5

    profile_controller.rate_profile(test_profile1.id, test_profile2.id, 2)
    assert test_profile2.times_rated == 1
    assert test_profile2.total_rating == 2
    assert test_profile2.average_rating == 2

    profile_controller.rate_profile(test_profile3.id, test_profile2.id, 2)
    assert test_profile2.times_rated == 2
    assert test_profile2.total_rating == 4
    assert test_profile2.average_rating == 2


def test_rate_picture(empty_db):
    test_profile1 = create_profile('test_rate_profile', 'password')
    test_profile2 = create_profile('test_rate_profile2', 'password')
    test_picture = Picture(url='test_rate_picture', profile=test_profile1)
    db.session.add(test_picture)
    db.session.commit()

    profile_controller.rate_picture(test_profile1.id, test_picture.id, 5)
    assert test_picture.times_rated == 1
    assert test_picture.total_rating == 5
    assert test_picture.average_rating == 5

    profile_controller.rate_profile(test_profile1.id, test_picture.id, 2)
    assert test_picture.times_rated == 1
    assert test_picture.total_rating == 2
    assert test_picture.average_rating == 2

    profile_controller.rate_profile(test_profile2.id, test_picture.id, 2)
    assert test_picture.times_rated == 2
    assert test_picture.total_rating == 4
    assert test_picture.average_rating == 2

# os.unlink(os.getcwd() + '/App/test.db')
# os.unlink(os.getcwd() + '/App/test_feed_config.json')
