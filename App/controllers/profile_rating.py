from App.models import *
from App.database import db

def create_profile_rating(rater, value):
    rating = ProfileRating(rater, value)
    db.session.add(rating)
    db.session.commit()
    return rating 