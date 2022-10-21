from App.controllers import tier
from App.database import db
from App.models import Picture, PictureRating, Profile, ProfileRating


def create_profile(username, password):
    if Profile.query.filter_by(username=username).first():
        return None
    profile = Profile(username, password)
    profile.remaining_views = tier.tier_info[1][1]
    db.session.add(profile)
    db.session.commit()
    return profile


def serialize_profiles(profile_list) -> dict:
    profiles = {}
    for _, profile in enumerate(profile_list):
        profiles[_] = profile.serialize()
    return profiles


def get_all_profiles():
    return Profile.query.all()


def get_profile(identifier):
    profile = None
    if isinstance(identifier, int):
        profile = Profile.query.get(identifier)
    elif isinstance(identifier, str):
        profile = Profile.query.filter_by(username=identifier).first()
    return profile


def get_picture(picture_id):
    picture = Picture.query.get(picture_id)
    return picture


def update_username(identifier, username):
    """Attempts to update a username. Returns False if profile does not exist or username is in use."""
    profile = get_profile(identifier)
    if profile and not get_profile(username):
        # profile.username = username
        profile.update_username(username)
        # db.session.add(profile)
        db.session.commit()
        return True
    return False


def upload_picture(identifier, url):
    """Adds a picture to a profile. Returns False if profile does not exist."""
    profile = get_profile(identifier)
    if profile:
        picture = Picture(url=url, profile=profile)
        db.session.add(picture)
        db.session.commit()
        return True
    return False


# def sort_pictures(pictures):
#     """Sorts pictures in order of highest to lowest rating."""
#     pictures.sort(key=lambda picture: picture.average_rating, reverse=True)
#     return pictures


def rate_profile(rater_id, ratee_id, value):
    rater: Profile = get_profile(rater_id)
    ratee: Profile = get_profile(ratee_id)

    if rater and ratee:
        rating = ProfileRating.query.get((rater_id, ratee_id))

        if rating:
            ratee.update_rating(value=value - rating.value, is_new=False)
            rating.value = value
        else:
            rating = ProfileRating(rater_id=rater.id, ratee_id=ratee.id, value=value)
            ratee.update_rating(value=value, is_new=True)
            rater.add_tier_point(tier.tier_info)
            db.session.add(rating)

        # db.session.add_all([rater, ratee, rating])
        db.session.commit()
        return True

    return False


def rate_picture(rater_id, ratee_id, value):
    rater = get_profile(rater_id)
    ratee = get_picture(ratee_id)

    if rater and ratee:
        rating = PictureRating.query.get((rater_id, ratee_id))

        if rating:
            ratee.update_rating(value=value - rating.value, is_new=False)
            rating.value = value
        else:
            rating = PictureRating(rater_id=rater.id, ratee_id=ratee.id, value=value)
            ratee.update_rating(value=value, is_new=True)
            db.session.add(rating)

        # db.session.add_all([rater, ratee, rating])
        db.session.commit()
        return True

    return False
