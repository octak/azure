from App.database import db
from App.models import *


def create_picture_rating(rater, value):
    rating = PictureRating(rater, value)
    db.session.add(rating)
    db.session.commit()
    return rating


def get_all_picture_ratings():
    return PictureRating.query.all()
