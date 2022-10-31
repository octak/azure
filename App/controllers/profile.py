from typing import Optional

from multimethod import multimethod
from sqlalchemy import func

from App.database import db
from App.models import Picture, PictureRating, User, ProfileRating


# Serialization #######################################################################################################

def to_dict_picture(picture: Picture) -> dict:
    return {
        "id": picture.id,
        'url': picture.url,
        'average_rating': get_average_rating_for_picture(picture.id)
    }


def to_dict_pictures(picture_list: list) -> dict:
    pictures = {}
    for _, picture in enumerate(picture_list):
        pictures[_] = to_dict_picture(picture)
    return pictures


def to_dict_user(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "tier": user.tier,
        "average_rating": get_average_rating_for_profile(user.id),
        "pictures": to_dict_pictures(user.pictures)
    }


def to_dict_users(user_list: list) -> dict:
    users = {}
    for _, user in enumerate(user_list):
        users[_] = to_dict_user(user)
    return users


# Services ############################################################################################################

def create_profile(username: str, password: str) -> Optional[User]:
    if not get_profile(username):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user
    return None


def create_picture(user_id: int, url: str) -> Optional[Picture]:
    user = get_profile(user_id)
    if user:
        post = Picture(user_id=user_id, url=url)
        db.session.add(post)
        db.session.commit()
        return post
    return None


def rate_profile(rater_id, rated_id, value):
    rater: User = get_profile(rater_id)
    rated: User = get_profile(rated_id)
    if not rater or not rated:
        return
    rating = get_profile_rating(rater_id, rated_id)
    if not rating:
        rating = ProfileRating(rater_id=rater.id, rated_id=rated.id, value=value)
        rater.increase_tier_points()
        db.session.add(rating)
    else:
        rating.value = value
    db.session.commit()


def rate_picture(rater_id, rated_id, value):
    rater = get_profile(rater_id)
    rated = get_picture(rated_id)
    if not rater or not rated:
        return
    rating = get_picture_rating(rater_id, rated_id)
    if not rating:
        rating = PictureRating(rater_id=rater.id, rated_id=rated.id, value=value)
        db.session.add(rating)
    else:
        rating.value = value
    db.session.commit()


def generate_feed():
    feed = []
    users = get_profiles()
    for user in users:
        if user.is_viewable():
            feed.append(user)
            user.decrease_remaining_views()
        db.session.commit()
    return feed


# Selectors ###########################################################################################################
def get_profiles() -> list:
    return db.session.scalars(db.select(User)).all()


@multimethod
def get_profile(user_id: int) -> Optional[User]:
    return db.session.scalars(db.select(User).where(User.id == user_id)).one_or_none()


@multimethod
def get_profile(username: str) -> Optional[User]:
    return db.session.scalars(db.select(User).where(User.username == username)).one_or_none()


def get_picture(post_id: int) -> Optional[Picture]:
    return db.session.scalars(db.select(Picture).where(Picture.id == post_id)).one_or_none()


def get_profile_rating(rater_id: int, object_id: int) -> Optional[ProfileRating]:
    return db.session.scalars(db.select(ProfileRating)
                              .where(ProfileRating.rater_id == rater_id,
                                     ProfileRating.rated_id == object_id)).one_or_none()


def get_picture_rating(rater_id: int, object_id: int) -> Optional[PictureRating]:
    return db.session.scalars(db.select(PictureRating)
                              .where(PictureRating.rater_id == rater_id,
                                     PictureRating.rated_id == object_id)).one_or_none()


def get_average_rating_for_profile(user_id: int) -> int:
    statement = db.session.query(func.avg(ProfileRating.value)).where(ProfileRating.rated_id == user_id)
    result = db.session.scalar(statement)
    return int(result) if result else 0


def get_average_rating_for_picture(post_id: int) -> int:
    statement = db.session.query(func.avg(PictureRating.value)).where(PictureRating.rated_id == post_id)
    result = db.session.scalar(statement)
    return int(result) if result else 0
