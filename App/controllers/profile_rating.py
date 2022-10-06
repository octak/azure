from App.models import *
from App.database import db

def create_profile_rating(rater, value):
    rating = ProfileRating(rater, value)
    db.session.add(rating)
    db.session.commit()
    return rating 

def get_all_profile_ratings():
    return ProfileRating.query.all()

def get_all_profiles_json():
    profiles = Profile.query.all()
    if not profiles:
        return []
    profiles = [profile.toJSON() for profile in profiles]
    return profiles