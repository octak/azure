from App.database import db
from App.models import Picture, PictureRating, Profile, ProfileRating


def create_profile(username, password):
    """Attempts to create a new profile. Returns None if username is in use."""
    if Profile.query.filter_by(username=username).first():
        return None
    profile = Profile(username=username, password=password)
    db.session.add(profile)
    db.session.commit()
    return profile


def get_all_profiles():
    return Profile.query.all()


def get_profile(identifier):
    if isinstance(identifier, int):
        profile = Profile.query.get(identifier)
    elif isinstance(identifier, str):
        profile = Profile.query.filter_by(username=identifier).first()
    return profile if profile else None


def update_username(identifier, username):
    """Attempts to update a username. Returns False if profile does not exist or username is in use."""
    profile = get_profile(identifier)
    if profile and not get_profile(username):
        profile.username = username
        db.session.add(profile)
        db.session.commit()
        return True
    return False


def upload_picture(identifier, url):
    """Adds a picture to a profile. Returns False if profile does not exist."""
    profile = get_profile(identifier)
    if not profile:
        return False
    picture = Picture(url=url, profile=profile)
    db.session.add(picture)
    db.session.commit()
    return True


def sort_pictures(pictures):
    """Sorts pictures in order of highest to lowest rating."""
    pictures.sort(key=lambda picture: picture.average_rating, reverse=True)
    return pictures


def get_uploaded_pictures(identifier):
    """Returns all pictures uploaded by the specified profile."""
    profile = get_profile(identifier)
    return profile.pictures if profile else []


def rate_profile(rater_id, ratee_id, value):
    rater = get_profile(rater_id)
    ratee = get_profile(ratee_id)
    if not rater or not ratee:
        return False
    rating = ProfileRating.query.get((rater_id, ratee_id))
    if rating:
        ratee.update_rating(rating.value - value)
        rating.value = value
    else:
        rating = ProfileRating(rater_id=rater.id, ratee_id=ratee.id, value=value)
        ratee.receive_rating(value)
        rater.increase_tier_points()
    db.session.add_all([rater, ratee, rating])
    db.session.commit()
    return True


def rate_picture(rater_id, ratee_id, value):
    rater = get_profile(rater_id)
    ratee = Picture.query.get(ratee_id)
    if not rater or not ratee:
        return False
    rating = PictureRating.query.get((rater_id, ratee_id))
    if rating:
        ratee.update_rating(rating.value - value)
        rating.value = value
    else:
        rating = PictureRating(rater_id=rater.id, ratee_id=ratee.id, value=value)
        ratee.receive_rating(value)
    db.session.add_all([rater, ratee, rating])
    db.session.commit()
    return True
