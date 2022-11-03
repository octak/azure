import logging
from datetime import datetime, timedelta

from App.controllers import *

LOGGER = logging.getLogger(__name__)


def test_create_user(new_user):
    test_time = datetime.now()

    assert new_user.username == 'username'
    assert new_user.password != 'password'
    assert new_user.tier == 1
    assert new_user.tier_points == 0
    assert new_user.remaining_views == 2
    assert new_user.last_refresh.date() == test_time.date()


def test_create_picture(new_picture):
    assert new_picture.id == 1
    assert new_picture.user_id == 1
    assert new_picture.url == "url"


def test_create_user_with_same_username(new_user):
    user = create_profile(new_user.username, 'password')
    assert user is None


def test_authenticate_user(new_user):
    assert new_user.check_password('password') is True
    assert new_user.check_password('not-the-password') is False


def test_increase_tier_points(new_user):
    for _ in range(4):
        new_user.increase_tier_points()

    assert new_user.tier == 2
    assert new_user.tier_points == 4
    assert new_user.remaining_views == 4


def test_decrease_remaining_views(new_user):
    for _ in range(2):
        new_user.decrease_remaining_views()

    assert new_user.remaining_views == 0
    assert not new_user.is_viewable()


def test_refresh_views(new_user):
    for _ in range(2):
        new_user.decrease_remaining_views()

    new_user.refresh_views()
    assert not new_user.is_viewable()

    delta = timedelta(days=1)
    new_user.last_refresh -= delta

    new_user.refresh_views()
    assert new_user.is_viewable()


def test_is_viewable(new_user):
    assert new_user.is_viewable()
    new_user.remaining_views = 0
    assert not new_user.is_viewable()


def test_serialize_user(new_user):
    expected_dict = {
        "id": 1,
        "username": "username",
        "tier": 1,
        "average_rating": 0,
        "pictures": {}
    }
    assert to_dict_profile(new_user) == expected_dict


def test_serialize_users(new_users):
    expected_dict = {
        0: {
            "id": 1,
            "username": "username1",
            "tier": 1,
            "average_rating": 0,
            "pictures": {}
        },
        1: {
            "id": 2,
            "username": "username2",
            "tier": 1,
            "average_rating": 0,
            "pictures": {}
        },
        2: {
            "id": 3,
            "username": "username3",
            "tier": 1,
            "average_rating": 0,
            "pictures": {}
        }
    }

    assert to_dict_profiles(new_users) == expected_dict
    assert to_dict_profiles([]) == {}


def test_serialize_picture(new_picture):
    expected_dict = {
        "id": 1,
        'url': "url",
        'average_rating': 0
    }

    assert to_dict_picture(new_picture) == expected_dict


def test_serialize_pictures(new_pictures):
    expected_dict = {
        0: {
            "id": 1,
            'url': "url1",
            'average_rating': 0
        },
        1: {
            "id": 2,
            'url': "url2",
            'average_rating': 0
        },
        2: {
            "id": 3,
            'url': "url3",
            'average_rating': 0
        }
    }

    assert to_dict_pictures(new_pictures) == expected_dict
    assert to_dict_pictures([]) == {}


def test_rate_user(new_users):
    user1 = new_users[0]
    user2 = new_users[1]

    rate_profile(user1.id, user2.id, 10)

    assert user1.tier_points == 1
    assert get_profile_rating(user1.id, user2.id).value == 10
    assert get_average_rating_for_profile(user2.id) == 10


def test_update_user_rating(new_users):
    user1 = new_users[0]
    user2 = new_users[1]

    rate_profile(user1.id, user2.id, 10)
    assert get_profile_rating(user1.id, user2.id).value == 10

    rate_profile(user1.id, user2.id, 20)
    assert get_profile_rating(user1.id, user2.id).value == 20

    assert user1.tier_points == 1
    assert get_average_rating_for_profile(user2.id) == 20


def test_rate_picture(new_picture_with_user):
    user = new_picture_with_user[0]
    picture = new_picture_with_user[1]

    rate_picture(user.id, picture.id, 10)

    assert get_picture_rating(user.id, picture.id).value == 10
    assert get_average_rating_for_picture(picture.id) == 10


def test_update_picture_rating(new_picture_with_user):
    user = new_picture_with_user[0]
    picture = new_picture_with_user[1]

    rate_picture(user.id, picture.id, 10)
    rate_picture(user.id, picture.id, 5)

    assert get_picture_rating(user.id, picture.id).value == 5
    assert get_average_rating_for_picture(picture.id) == 5


def test_generate_feed(new_users):
    feed = generate_feed()

    assert len(feed) == len(new_users)

    for id, user in enumerate(feed, start=1):
        assert user.id == id
        assert user.remaining_views == 1


def test_get_users(new_users):
    users = get_profiles()

    for _, user in enumerate(users):
        assert user == new_users[_]


def test_get_user(new_user):
    assert get_profile(new_user.id) == new_user
    assert get_profile(new_user.username) == new_user


def test_get_picture(new_picture):
    assert get_picture(new_picture.id) == new_picture
