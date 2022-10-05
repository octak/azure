from App.models import *
from App.database import db

def create_picture(url):
    picture = Picture(url)
    db.session.add(picture)
    db.session.commit()
    return picture

def get_all_pictures_json():
    pictures = Picture.query.all()
    if not pictures:
        return []
    pictures = [picture.toJSON() for picture in pictures]
    return pictures

def add_rating_to_picture(pictureID, ratingID):
    picture = Picture.query.filter_by(id=pictureID).first()
    rating = PictureRating.query.filter_by(id=ratingID).first()
    picture.ratings.append(rating)
    db.session.commit()

def add_rating_to_profile(pictureID, ratingID):
    rating = PictureRating.query.filter_by(id=ratingID).first()
    rated_picture = Picture.query.filter_by(id=pictureID).first()
    rated_profile.ratings.append(rating)
    rated_profile.increase_rating(rating.value)
    db.session.commit()