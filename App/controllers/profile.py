import json
from functools import singledispatch

from App.controllers import *
from App.database import db
from App.models import *


def create_profile(username, password):
    '''Attempts to create a new profile. Returns None if username is in use.'''
    if Profile.query.filter_by(username=username).first():
        return None
    new_profile = Profile(username=username, password=password)
    db.session.add(new_profile)
    db.session.commit()
    return new_profile


def jsonify_(items):
    '''Returns JSON representation of supplied objects.'''
    return [item.toJSON() for item in items] if items else []


def get_all_profiles():
    '''Returns a list of all profiles. '''
    return Profile.query.all()

@singledispatch
def get_profile(key):
    raise NotImplementedError

@get_profile.register
def _(key: int):
    '''Returns profile represented by the supplied ID. '''
    return Profile.query.get(key)


@get_profile.register
def _(key: str):
    '''Returns profile represented by the supplied username.'''
    return Profile.query.filter_by(username=key).first()




def update_username(key, username):
    '''Attempts to update a username. Returns False if profile does not exist or username is in use.'''
    profile = get_profile(key)
    if profile and not get_profile(username):
        profile.username = username
        db.session.add(profile)
        db.session.commit()
        return True
    return False


def upload_picture(key, url):
    '''Adds a picture to a profile. Returns False if profile does not exist.'''
    profile = get_profile(key)
    if not profile:
        return False
    picture = Picture(url=url, profile=profile)
    db.session.add(picture)
    db.session.commit()
    return True


def sort_pictures(pictures):
    '''Sorts pictures in order of highest to lowest rating.'''
    pictures.sort(key=lambda picture: picture.average_rating, reverse=True)
    return pictures


def get_all_pictures(key):
    '''Returns all pictures uploaded by the specified profile.'''
    profile = get_profile(key)
    return profile.pictures if profile else []


def get_rated_profiles(key):
    '''Returns all pictures rated by the specified profile.'''
    profile = get_profile(key)
    return profile.rated_profiles if profile else []


def get_rated_pictures(key):
    '''Returns all profiles rated by the specified profile.'''
    profile = get_profile(key)
    return profile.rated_profiles if profile else []


def get_raters(key):
    '''Returns all profiles which rated the specified profile.'''
    profile = get_profile(key)
    return profile.ratings if profile else []


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
        rating = ProfileRating(rater=rater, ratee=ratee, value=value)
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
        rating = PictureRating(rater=rater, ratee=ratee, value=value)
        ratee.receive_rating(value)
    db.session.add_all([rater, ratee, rating])
    db.session.commit()
    return True
