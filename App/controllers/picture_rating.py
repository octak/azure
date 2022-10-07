from App.models import *
from App.database import db

def create_picture_rating(rater, value):
    """ Do we need this one? """
    rating = PictureRating(rater, value)
    db.session.add(rating)
    db.session.commit()
    return rating
