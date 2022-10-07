from App.database import db
from App.models import *

# def get_all_profiles_json():
#     profiles = Profile.query.all()
#     if not profiles:
#         return []
#     profiles = [profile.toJSON() for profile in profiles]
#     return profiles

def create_profile_rating(raterID, value):
    rating = ProfileRating(raterID, value)
    db.session.add(rating)
    db.session.commit()
    return rating 

def get_all_profile_ratings():
    return ProfileRating.query.all()
